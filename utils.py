def calcular_tempo_medio_espera(total_tempo_espera, clientes_atendidos):
    """Tempo médio de espera dos clientes."""
    if clientes_atendidos == 0:
        return 0
    return total_tempo_espera / clientes_atendidos
