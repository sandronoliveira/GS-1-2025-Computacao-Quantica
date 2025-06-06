from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def run_quantum_rescue_simulation():
    """
    Simula um processo de tomada de decisão quântica para a priorização da resposta a desastres.
    """

    # --- 1. Define Registradores Quânticos e Clássicos ---
    # Qubits de sensor para a Zona A (sA[0]=Severidade, sA[1]=Vítimas)
    qr_sensors_A = QuantumRegister(2, 'sA')
    # Qubits de sensor para a Zona B (sB[0]=Severidade, sB[1]=Vítimas)
    qr_sensors_B = QuantumRegister(2, 'sB')
    # Qubit ancilla para a prioridade da Zona A
    qr_priority_A = QuantumRegister(1, 'pA')
    # Qubit ancilla para a prioridade da Zona B
    qr_priority_B = QuantumRegister(1, 'pB')
    # Qubit para a decisão final (1 para Zona A, 0 para Zona B)
    qr_decision = QuantumRegister(1, 'decision')

    # Registrador clássico para armazenar a medição do qubit de decisão
    cr_result = ClassicalRegister(1, 'c_decision')

    # --- 2. Cria o Circuito Quântico ---
    qc = QuantumCircuit(qr_sensors_A, qr_sensors_B, qr_priority_A, qr_priority_B, qr_decision, cr_result)

    # --- 3. Superposição para as Entradas dos Sensores ---
    # Coloca todos os qubits de sensor em superposição para representar incerteza ou explorar todos os cenários
    qc.h(qr_sensors_A[0])  # Severidade Zona A
    qc.h(qr_sensors_A[1])  # Vítimas Zona A
    qc.h(qr_sensors_B[0])  # Severidade Zona B
    qc.h(qr_sensors_B[1])  # Vítimas Zona B
    qc.barrier() # Separador visual e de compilação

    # --- 4. Emaranhamento para Sensores Interdependentes ---
    # Modela a interdependência: se a severidade é alta (1), isso influencia a avaliação de vítimas.
    # Ex: Se sA[0] (Severidade A) é |1>, sA[1] (Vítimas A) é invertido.
    # Isso visa criar uma correlação, por exemplo, (Alta Severidade, Muitas Vítimas) ou
    # (Alta Severidade, Poucas Vítimas) se tornam mais prováveis do que (Baixa Severidade, Muitas Vítimas).
    # Nota: Esta é uma forma simplificada de modelar correlação.
    qc.cx(qr_sensors_A[0], qr_sensors_A[1])
    qc.cx(qr_sensors_B[0], qr_sensors_B[1])
    qc.barrier()

    # --- 5. Calcula a Prioridade para a Zona A (pA) ---
    # pA = 1 se (Severidade A = 1 AND Vítimas A = 1)
    # Usa porta Toffoli (CCX): pA[0] inverte se sA[0]=1 e sA[1]=1.
    # qr_priority_A[0] é inicializado em |0>.
    qc.ccx(qr_sensors_A[0], qr_sensors_A[1], qr_priority_A[0])
    qc.barrier()

    # --- 6. Calcula a Prioridade para a Zona B (pB) ---
    # pB = 1 se (Severidade B = 1 AND Vítimas B = 1)
    # Usa porta Toffoli (CCX): pB[0] inverte se sB[0]=1 e sB[1]=1.
    # qr_priority_B[0] é inicializado em |0>.
    qc.ccx(qr_sensors_B[0], qr_sensors_B[1], qr_priority_B[0])
    qc.barrier()

    # --- 7. Lógica de Decisão para qr_decision[0] (1 para Zona A, 0 para Zona B) ---
    # Lógica: Priorizar A se pA=1. Senão, priorizar B se pB=1. Senão (nenhuma é prioritária), priorizar A.
    # Isso se traduz em: decision = pA OR (!pA AND !pB)
    # O qubit qr_decision[0] é inicializado em |0>.

    # Parte 1: Se pA = 1, então decision = 1.
    qc.cx(qr_priority_A[0], qr_decision[0])

    # Parte 2: Se pA = 0 E pB = 0, então decision = 1 (para implementar o padrão para A)
    # Usamos CCX com controles invertidos para pA e pB sobre qr_decision[0].
    # Se qr_decision[0] é 0 (porque pA=0), e pA original=0 e pB original=0, então decision se torna 1.
    qc.x(qr_priority_A[0]) # Inverte pA: agora é 1 se o pA original era 0
    qc.x(qr_priority_B[0]) # Inverte pB: agora é 1 se o pB original era 0
    qc.ccx(qr_priority_A[0], qr_priority_B[0], qr_decision[0])
    qc.x(qr_priority_A[0]) # Desfaz a inversão de pA
    qc.x(qr_priority_B[0]) # Desfaz a inversão de pB
    qc.barrier()

    # --- 8. Mede o Qubit de Decisão ---
    qc.measure(qr_decision[0], cr_result[0])

    # --- 9. Simula o Circuito ---
    print("Circuito Quântico para Tomada de Decisão:")
    try:
        circuit_diagram = qc.draw(output='mpl')
        circuit_diagram.savefig("quantum_circuit_diagram.png")
        print("\nDiagrama do circuito salvo como quantum_circuit_diagram.png")
    except Exception as e:
        print(f"Não foi possível gerar o diagrama do circuito em formato de imagem (matplotlib): {e}")
        print("Mostrando diagrama em texto:")
        print(qc.draw(output='text'))

    print("\nSimulando o circuito...")
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=8192) # Aumentar shots para melhor estatística
    result = job.result()
    counts = result.get_counts(qc)

    print("\nResultados da Simulação (Contagens):")
    print(counts)
    print("\nInterpretação dos Resultados:")
    print("'0' significa priorizar Zona B.")
    print("'1' significa priorizar Zona A.")

    # Gerar e salvar histograma
    try:
        fig = plot_histogram(counts)
        fig.savefig("results_histogram.png")
        print("Histograma dos resultados salvo como results_histogram.png")
        # plt.show() # Descomente se quiser exibir o gráfico interativamente
    except Exception as e:
        print(f"Não foi possível gerar o histograma (matplotlib): {e}")
        print("Histograma não pôde ser salvo como imagem. Contagens impressas acima.")

    return qc, counts

if __name__ == '__main__':
    qc_final, result_counts = run_quantum_rescue_simulation()
    print("\nExecução da simulação concluída.")
    if result_counts:
        print(f"Contagens finais: {result_counts}")
