import random
from collections import defaultdict

from randomNumberGenerator import NextRandom

# Inicializa filas e dados da simulação
filas = {"q1": [], "q2": [], "q3": []}
clientes_perdidos = {"q2": 0, "q3": 0}
times = {"q1": defaultdict(int), "q2": defaultdict(int), "q3": defaultdict(int)}
tempo_global = 0

# Parâmetros iniciais (serão lidos do arquivo de configuração)
parametros_filas = {}

def carregar_parametros(arquivo_config):
    """Carrega os parâmetros das filas a partir de um arquivo de configuração."""
    global parametros_filas

    with open(arquivo_config, 'r') as f:
        parametros = eval(f.read())  # Cuidado: em um ambiente real, use uma abordagem segura!

    parametros_filas = parametros["queues"]

def gerar_tempo(min_val, max_val):
    """Gera um tempo aleatório entre min_val e max_val."""
    return int(min_val + (max_val - min_val) * NextRandom())

# Funções flexíveis para tempo de chegada e atendimento
def tempo_chegada_q1():
    """Gera tempo entre chegadas para Q1."""
    min_arrival = parametros_filas["q1"]["minArrival"]
    max_arrival = parametros_filas["q1"]["maxArrival"]
    return gerar_tempo(min_arrival, max_arrival)

def tempo_atendimento_q1():
    """Gera tempo de atendimento para Q1."""
    min_service = parametros_filas["q1"]["minService"]
    max_service = parametros_filas["q1"]["maxService"]
    return gerar_tempo(min_service, max_service)

def tempo_atendimento_q2():
    """Gera tempo de atendimento para Q2."""
    min_service = parametros_filas["q2"]["minService"]
    max_service = parametros_filas["q2"]["maxService"]
    return gerar_tempo(min_service, max_service)

def tempo_atendimento_q3():
    """Gera tempo de atendimento para Q3."""
    min_service = parametros_filas["q3"]["minService"]
    max_service = parametros_filas["q3"]["maxService"]
    return gerar_tempo(min_service, max_service)

def chegada_q1():
    """Lógica de chegada na fila Q1."""
    filas["q1"].append(tempo_atendimento_q1())

def saida_q1():
    """Lógica de saída da fila Q1."""
    if filas["q1"]:
        cliente = filas["q1"].pop(0)  # Cliente sai da fila 1
        prob = random.random()
        if prob < 0.8:  # 80% vão para Q2
            if len(filas["q2"]) < parametros_filas["q2"]["capacity"]:
                filas["q2"].append(tempo_atendimento_q2())
            else:
                clientes_perdidos["q2"] += 1
        else:  # 20% vão para Q3
            if len(filas["q3"]) < parametros_filas["q3"]["capacity"]:
                filas["q3"].append(tempo_atendimento_q3())
            else:
                clientes_perdidos["q3"] += 1

def saida_q2():
    """Lógica de saída da fila Q2."""
    if filas["q2"]:
        cliente = filas["q2"].pop(0)
        prob = random.random()
        if prob < 0.8:
            if prob < 0.3:  # 50% voltam para Q1
                filas["q1"].append(tempo_atendimento_q1())
            elif prob < 0.5:  # 30% vão para Q3
                if len(filas["q3"]) < parametros_filas["q3"]["capacity"]:
                    filas["q3"].append(tempo_atendimento_q3())
                else:
                    clientes_perdidos["q3"] += 1

        # 20% saem do sistema (nada acontece)

def saida_q3():
    """Lógica de saída da fila Q3."""
    if filas["q3"]:
        cliente = filas["q3"].pop(0)
        if random.random() < 0.7:  # 70% voltam para Q2
            if len(filas["q2"]) < parametros_filas["q2"]["capacity"]:
                filas["q2"].append(tempo_atendimento_q2())
            else:
                clientes_perdidos["q2"] += 1
        # 30% saem do sistema (nada acontece)

def processar_eventos():
    """Processa todos os eventos nas filas."""
    global tempo_global

    if filas["q1"]:
        saida_q1()
    if filas["q2"]:
        saida_q2()
    if filas["q3"]:
        saida_q3()

    for nome_fila in times:
        estado = len(filas[nome_fila])
        times[nome_fila][estado] += 1

    tempo_global += 1

def simulador():
    """Executa a simulação."""
    global tempo_global

    proxima_chegada_q1 = 2  # Primeiro cliente chega no tempo 2,0

    for _ in range(100000):  # 100.000 eventos
        if tempo_global >= proxima_chegada_q1:
            chegada_q1()
            proxima_chegada_q1 += tempo_chegada_q1()

        processar_eventos()

    reportar_resultados()

def reportar_resultados():
    """Exibe os resultados da simulação."""
    print("=== Resultados da Simulação ===")
    for nome_fila in times:
        print(f"\nFila {nome_fila.upper()}")
        for estado, tempo in sorted(times[nome_fila].items()):
            porcentagem = (tempo / tempo_global) * 100
            print(f"Estado {estado}: {tempo} ({porcentagem:.2f}%)")

    print("\nClientes perdidos:")
    total_perdidos = sum(clientes_perdidos.values())
    print(f"Total: {total_perdidos}")

    print(f"\nTempo global da simulação: {tempo_global} minutos")

if __name__ == "__main__":
    carregar_parametros("config.txt")  # Carrega os parâmetros do arquivo
    simulador()
