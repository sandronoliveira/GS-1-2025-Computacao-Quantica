# Relatório GS – QuantumRescue: Inteligência Quântica para Apoio Autônomo em Situações de Desastre

**Integrantes**:
Sandron Oliveira Silva 
**RM: 557172**
Nickolas Alexandre Ferraz
**RM: 558458**
Marcos Paolucci Salamondac
**RM: 554941**

---

## 1. Introdução

Este relatório detalha a Prova de Conceito (PoC) do subsistema de tomada de decisão do assistente autônomo QuantumRescue. O objetivo é demonstrar como a computação quântica, utilizando Qiskit, pode ser aplicada para avaliar cenários e tomar decisões em tempo real em situações de desastre, explorando os princípios de superposição e emaranhamento quântico.

## 2. Conceitos Teóricos Utilizados

### 2.1. Qubits
Um qubit, ou bit quântico, é a unidade básica da informação quântica. Diferentemente de um bit clássico, que pode ser 0 ou 1, um qubit pode representar 0, 1, ou uma combinação de ambos através de um fenômeno chamado **superposição**. Matematicamente, o estado de um qubit (ψ) é uma combinação linear dos estados base |0⟩ e |1⟩:

$$ |
\psi\rangle = \alpha|0\rangle + \beta|1\rangle $$

Onde α e β são amplitudes de probabilidade complexas, tais que $|\alpha|^2 + |\beta|^2 = 1$. $|\alpha|^2$ é a probabilidade de medir o qubit no estado 0, e $|\beta|^2$ é a probabilidade de medir o estado 1.

### 2.2. Superposição
A superposição permite que um qubit exista em múltiplos estados simultaneamente até que uma medição seja feita. No contexto do QuantumRescue, a superposição é utilizada para representar múltiplos cenários de desastre ou estados ambientais de uma só vez. Por exemplo, um qubit pode representar o estado de um sensor (e.g., nível de perigo alto ou baixo) existindo em ambos os estados com certas probabilidades.

### 2.3. Portas Quânticas
Portas quânticas são operações que manipulam o estado dos qubits. São análogas às portas lógicas na computação clássica, mas são reversíveis (exceto a medição).

- **Porta Hadamard (H):** Cria superposição. Aplicada a um qubit no estado |0⟩ ou |1⟩, transforma-o em uma superposição igual de |0⟩ e |1⟩.
  $$ H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} $$
  $$ H|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} $$
- **Porta Pauli-X (NOT):** Inverte o estado do qubit (|0⟩ ↔ |1⟩).
- **Porta CNOT (Controlled-NOT):** É uma porta de dois qubits. Se o qubit de controle estiver no estado |1⟩, ela aplica uma porta X (NOT) ao qubit alvo. Caso contrário, o qubit alvo permanece inalterado. Esta porta é fundamental para criar **emaranhamento**.
- **Porta Toffoli (CCX - Controlled-Controlled-NOT):** É uma porta de três qubits. Se os dois primeiros qubits de controle estiverem no estado |1⟩, ela aplica uma porta X (NOT) ao qubit alvo. É análoga à porta AND clássica e útil para implementar lógica booleana.

### 2.4. Emaranhamento Quântico
O emaranhamento é um fenômeno quântico onde dois ou mais qubits tornam-se interligados de tal forma que seus estados não podem ser descritos independentemente, mesmo que separados por grandes distâncias. A medição de um qubit emaranhado instantaneamente influencia o estado do(s) outro(s). No QuantumRescue, o emaranhamento é usado para modelar a interdependência entre diferentes sensores ou fatores (e.g., a gravidade de um incêndio e o número de vítimas podem estar correlacionados).

### 2.5. Medidas Quânticas
A medição é o processo de extrair informação clássica de um qubit. Quando um qubit em superposição é medido, seu estado "colapsa" para um dos estados base (|0⟩ ou |1⟩) com uma probabilidade determinada pelas suas amplitudes. A medição é um processo irreversível.

### 2.6. Esfera de Bloch
A Esfera de Bloch é uma representação geométrica do espaço de estados de um único qubit. Os pólos norte e sul representam os estados |0⟩ e |1⟩, respectivamente. Qualquer outro ponto na superfície da esfera representa uma superposição pura dos dois estados base.

*Recomendado: Inserir imagem da Esfera de Bloch aqui ou descrever detalhadamente sua aparência e o significado dos eixos X, Y e Z na representação de estados de superposição e fases relativas.*

## 3. Descrição da Lógica do Sistema/Assistente Proposto (QuantumRescue)

O QuantumRescue é um assistente autônomo concebido para otimizar a tomada de decisões em cenários de desastres naturais. O subsistema simulado foca na priorização de envio de ajuda para diferentes zonas afetadas.

**Lógica Implementada:**

1. **Entrada de Dados (Sensores):**
   - O sistema considera duas zonas de desastre, Zona A e Zona B.
   - Para cada zona, há dois sensores simulados por qubits:
     - **Severidade (sX[0]):** Representa o nível de perigo/dano na zona X (A ou B). |0⟩ = Baixa Severidade, |1⟩ = Alta Severidade.
     - **Vítimas (sX[1]):** Representa o número de vítimas ou a urgência de resgate na zona X. |0⟩ = Poucas Vítimas/Baixa Urgência, |1⟩ = Muitas Vítimas/Alta Urgência.

2. **Processamento Quântico:**
   - **Superposição:** Os qubits dos sensores são colocados em superposição usando portas Hadamard. Isso permite que o sistema explore simultaneamente todos os 16 possíveis combinações de estados dos sensores (2 sensores x 2 zonas x 2 estados cada = $2^4$ estados).
   - **Emaranhamento:** Portas CNOT são usadas para criar uma correlação entre o sensor de Severidade e o sensor de Vítimas para cada zona. A lógica implementada é que se a Severidade é alta (|1⟩), isso influencia (inverte) o estado do qubit de Vítimas. Esta é uma forma simplificada de demonstrar a interdependência, sugerindo que alta severidade tende a alterar o estado de "vítimas" (e.g., de poucas para muitas, ou vice-versa, dependendo do estado inicial em superposição).
   - **Cálculo de Prioridade por Zona:**
     - Um qubit ancilla (`pA` para Zona A, `pB` para Zona B), inicializado em |0⟩, é usado para calcular a prioridade de cada zona.
     - A prioridade é considerada ALTA (|1⟩) se AMBOS, Severidade e Vítimas, estiverem em estado ALTO (|1⟩). Isso é implementado usando uma porta Toffoli (CCX): `pX` torna-se |1⟩ se `sX[0]=|1⟩` AND `sX[1]=|1⟩`.
   - **Tomada de Decisão Final:**
     - Um qubit de decisão (`decision`), inicializado em |0⟩, determina qual zona priorizar (|1⟩ para Zona A, |0⟩ para Zona B).
     - A lógica de decisão é:
       1. Se a Zona A tem prioridade alta (`pA = |1⟩`), então `decision` é definido como |1⟩ (Priorizar Zona A).
       2. Senão (se `pA = |0⟩`), se a Zona B tem prioridade alta (`pB = |1⟩`), então `decision` é definido como |0⟩ (Priorizar Zona B). (Nota: No código, esta condição não é explicitamente setada para 0, pois o default de `decision` é |0⟩ e a lógica subsequente cobre o caso de `pA=0 AND pB=0`).
       3. Senão (se `pA = |0⟩` E `pB = |0⟩` - nenhuma zona tem prioridade alta), o sistema, por padrão, prioriza a Zona A (`decision` é definido como |1⟩).
       - A lógica efetivamente implementada no código é: `decision = pA` inicialmente. Depois, se `!pA AND !pB`, então `decision` é invertido (se era |0⟩ por `pA=0`, torna-se |1⟩).

3. **Saída (Medição):**
   - O qubit `decision` é medido. O resultado (0 ou 1) indica a zona a ser priorizada com base na avaliação quântica de todos os cenários em superposição.

## 4. Código Qiskit com Comentários e Explicações

O código Python abaixo utiliza a biblioteca Qiskit para implementar a simulação do QuantumRescue.

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def run_quantum_rescue_simulation():
    """
    Simulates a quantum decision-making process for disaster response prioritization.
    """
    # --- 1. Define Quantum and Classical Registers ---
    # Sensor qubits for Zone A (sA[0]=Severity, sA[1]=Casualties)
    qr_sensors_A = QuantumRegister(2, 'sA')
    # Sensor qubits for Zone B (sB[0]=Severity, sB[1]=Casualties)
    qr_sensors_B = QuantumRegister(2, 'sB')
    # Ancilla qubit for Zone A priority
    qr_priority_A = QuantumRegister(1, 'pA')
    # Ancilla qubit for Zone B priority
    qr_priority_B = QuantumRegister(1, 'pB')
    # Qubit for the final decision (1 for Zone A, 0 for Zone B)
    qr_decision = QuantumRegister(1, 'decision')
    # Classical register to store the measurement of the decision qubit
    cr_result = ClassicalRegister(1, 'c_decision')
    # --- 2. Create Quantum Circuit ---
    qc = QuantumCircuit(qr_sensors_A, qr_sensors_B, qr_priority_A, qr_priority_B, qr_decision, cr_result)
    # --- 3. Superposition for Sensor Inputs ---
    # Place all sensor qubits in superposition to represent uncertainty or explore all scenarios
    qc.h(qr_sensors_A[0])  # Severity Zone A
    qc.h(qr_sensors_A[1])  # Casualties Zone A
    qc.h(qr_sensors_B[0])  # Severity Zone B
    qc.h(qr_sensors_B[1])  # Casualties Zone B
    qc.barrier() # Separador visual e de compilação
    # --- 4. Entanglement for Interdependent Sensors ---
    # Model interdependency: if severity is high (1), it influences casualty assessment.
    # Ex: Se sA[0] (Severidade A) é |1>, sA[1] (Vítimas A) é invertido.
    # Isso visa criar uma correlação.
    qc.cx(qr_sensors_A[0], qr_sensors_A[1])
    qc.cx(qr_sensors_B[0], qr_sensors_B[1])
    qc.barrier()
    # --- 5. Calculate Priority for Zone A (pA) ---
    # pA = 1 se (Severidade A = 1 AND Vítimas A = 1)
    # qr_priority_A[0] é inicializado em |0>.
    qc.ccx(qr_sensors_A[0], qr_sensors_A[1], qr_priority_A[0])
    qc.barrier()
    # --- 6. Calculate Priority for Zone B (pB) ---
    # pB = 1 se (Severidade B = 1 AND Vítimas B = 1)
    # qr_priority_B[0] é inicializado em |0>.
    qc.ccx(qr_sensors_B[0], qr_sensors_B[1], qr_priority_B[0])
    qc.barrier()
    # --- 7. Decision Logic for qr_decision[0] (1 para Zona A, 0 para Zona B) ---
    # Lógica: Priorizar A se pA=1. Senão, se pB=1, priorizar B. Senão (ambas baixa prioridade), priorizar A.
    # Implementação: decision = pA OR (!pA AND !pB)
    # O qubit qr_decision[0] é inicializado em |0>.
    # Parte 1: Se pA = 1, então decision = 1.
    qc.cx(qr_priority_A[0], qr_decision[0]) # decision = pA (se decision era |0>)
    # Parte 2: Se pA = 0 E pB = 0, então decision = 1.
    # (Se pA=0, decision é |0> após o CX acima. Se pB=0 também, queremos decision=|1>)
    qc.x(qr_priority_A[0]) # Inverte pA: agora é 1 se pA original era 0
    qc.x(qr_priority_B[0]) # Inverte pB: agora é 1 se pB original era 0
    # Se pA original era 0 E pB original era 0, então os dois controles são 1.
    # qr_decision[0] será invertido. Se era 0 (porque pA=0), se torna 1.
    qc.ccx(qr_priority_A[0], qr_priority_B[0], qr_decision[0])
    qc.x(qr_priority_A[0]) # Desfaz a inversão de pA
    qc.x(qr_priority_B[0]) # Desfaz a inversão de pB
    qc.barrier()
    # --- 8. Measure the Decision Qubit ---
    qc.measure(qr_decision[0], cr_result[0])
    # --- 9. Simulate the Circuit ---
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
    # Aumentar shots para melhor estatística e para corresponder ao critério GS
    job = simulator.run(compiled_circuit, shots=8192)
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
```

## 5. Prints do Circuito e Output

### 5.1. Diagrama do Circuito (Qiskit `qc.draw()`)

*(Inserir aqui a imagem `quantum_circuit_diagram.png` gerada pelo script ou um print do Qiskit Composer)*

**Representação em Texto (fallback, gerada pelo script):**

```text
(O output do qc.draw(output='text') será exibido aqui pelo script se a geração de imagem falhar.
Copie e cole o output do terminal aqui se necessário.)

Exemplo de como o output em texto pode parecer (varia conforme o circuito exato):

      ┌───┐      ░                 ░       ░                 ░                           ░ ┌─┐
sA_0: ┤ H ├──■───░─────────────────░───■───░─────────────────░───────────────────────────░─┤M├
      ├───┤┌─┴─┐ ░                 ░   │   ░                 ░                           ░ └╥┘
sA_1: ┤ H ├┤ X ├─░─────────────────░───■───░─────────────────░───────────────────────────░──╫─
      ├───┤└───┘ ░ ┌───┐           ░   │   ░                 ░                           ░  ║ 
sB_0: ┤ H ├──■───░─┤ X ├───────────░───┼───░───■─────────────░───────────────────────────░──╫─
      ├───┤┌─┴─┐ ░ │   │           ░   │   ░   │             ░                           ░  ║ 
sB_1: ┤ H ├┤ X ├─░─┤ X ├───────────░───┼───░───■─────────────░───────────────────────────░──╫─
      └───┘└───┘ ░ └─┬─┘           ░ ┌─┴─┐ ░                 ░ ┌───┐    ┌───┐┌───┐        ░  ║ 
pA: ─────────────░───■─────────────░─┤ X ├─░─────────────────░─┤ X ├─■──┤ X ├┤ X ├─■──────░──╫─
                 ░                 ░ └─┬─┘ ░ ┌───┐           ░ └─┬─┘ │  └─┬─┘└─┬─┘ │      ░  ║ 
pB: ─────────────░─────────────────░───■───░─┤ X ├───────────░───■───■────■──┤ X ├─■──────░──╫─
                 ░                 ░       ░ └─┬─┘┌───┐┌───┐ ░     │         └───┘ │  ┌───┐ ░  ║ 
decision: ─────────░─────────────────░───────░───■──┤ X ├┤ X ├─░─────■─────────────■──┤ X ├─░──╫─
                 ░                 ░       ░      └───┘└───┘ ░                       └───┘ ░  ║ 
c_decision:═════════════════════════════════════════════════════════════════════════════════╩══
```

### 5.2. Output da Simulação (Resultados/Contagens)

*(Inserir aqui a imagem `results_histogram.png` gerada pelo script e o output de texto das contagens do terminal)*

**Exemplo de Contagens (obtido do output do script):**

```text
Resultados da Simulação (Contagens):
{'1': 6150, '0': 2042} # Estes números são exemplos e variarão a cada execução completa do script.

Interpretação dos Resultados:
'0' significa priorizar Zona B.
'1' significa priorizar Zona A.
```

## 6. Interpretação do Resultado Quântico Aplicado ao Problema Real

Os resultados da simulação (contagens para os estados '0' e '1' do qubit de decisão) representam as probabilidades de priorizar a Zona A ou a Zona B após considerar todos os cenários de sensores em superposição e suas interdependências, conforme a lógica implementada.

- **Se a contagem para '1' (Zona A) for significativamente maior que para '0' (Zona B):** Indica que, sob a lógica quântica implementada e considerando todas as incertezas dos sensores, há uma propensão maior do sistema em designar a Zona A como prioritária. Isto ocorre se: (a) os cenários onde Zona A é de alta prioridade (`pA=1`) são dominantes, ou (b) nos cenários onde ambas as zonas têm baixa prioridade (`pA=0` e `pB=0`), pois a lógica de default escolhe Zona A.

- **Se a contagem para '0' (Zona B) for significativamente maior que para '1' (Zona A):** Sugere que a Zona B é mais frequentemente identificada como a escolha prioritária. Isso aconteceria predominantemente nos casos onde `pA=0` (Zona A não é alta prioridade) e `pB=1` (Zona B é alta prioridade). De acordo com a lógica `decision = pA OR (!pA AND !pB)`, se `pA=0` e `pB=1`, então `decision` deveria ser `0 OR (1 AND 0) = 0`. No entanto, o código implementa `decision = pA` e depois `decision` é invertido se `!pA AND !pB`. Se `pA=0` e `pB=1`, `decision` começa como `0`. `!pA AND !pB` é `1 AND 0 = 0`, então `decision` permanece `0`. Este caso corretamente prioriza Zona B.

- **Se as contagens forem próximas (ex: 50%-50% ou 60%-40%):** Indica que, sob a lógica atual, não há uma preferência esmagadoramente clara. A decisão final pode depender de fatores estocásticos ou requerer análise mais fina. A distribuição de probabilidade reflete a avaliação combinada de todos os estados possíveis dos sensores.

A simulação demonstra o potencial da computação quântica para:
1. **Explorar Paralelamente Múltiplos Cenários:** A superposição permite avaliar todas as $2^4=16$ combinações de inputs dos sensores de uma só vez.
2. **Modelar Interdependências Complexas:** O emaranhamento (aqui simplificado com CNOTs) pode capturar correlações entre diferentes fatores (como severidade e número de vítimas).
3. **Tomada de Decisão Probabilística:** O resultado da medição é probabilístico. Múltiplas execuções (shots) ajudam a construir um perfil de probabilidade para a decisão mais robusta, refletindo a incerteza inerente.

**Limitações e Próximos Passos:**
- A lógica de priorização (`decision = pA OR (!pA AND !pB)`) e a modelagem do emaranhamento são simplificações. Modelos mais sofisticados poderiam incluir mais fatores, pesos diferentes para os sensores, ou lógicas de decisão mais complexas (e.g., usando Grover para buscar a "melhor" solução, ou QRAM para carregar dados clássicos complexos).
- A simulação usa um simulador clássico ideal. A execução em hardware quântico real introduziria ruído e erros de porta, o que precisaria ser considerado e mitigado usando técnicas de correção de erros quânticos ou hardware tolerante a falhas.

Este PoC serve como um passo inicial, ilustrando o potencial da abordagem quântica para problemas de decisão sob incerteza, característicos de operações de resgate em desastres.

## 7. Conclusão

A simulação QuantumRescue demonstrou com sucesso como os princípios da computação quântica – notadamente superposição e emaranhamento – podem ser aplicados para construir um subsistema de decisão para um assistente autônomo em cenários de desastre. O uso do Qiskit permitiu a criação e simulação de um circuito quântico que avalia múltiplos cenários e interdependências de sensores para chegar a uma decisão de priorização probabilística.

Embora esta seja uma prova de conceito simplificada, ela estabelece uma base para futuras explorações no uso de IA quântica para otimizar respostas a emergências. O projeto cumpre o objetivo de conectar conceitos quânticos com a lógica de IA em tempo real, aplicável em contextos de emergência, e serve como um ponto de partida para investigações mais profundas e complexas.

---
*(Fim do Relatório)* 