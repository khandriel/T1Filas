# randomNumberGenerator.py
# Gerador LCG modificado com a função NextRandom

seed = 42  # Semente inicial
a = 1664525  
c = 1013904223  
m = 2**32  
last_random = seed  # Armazena o último número gerado

def NextRandom():
    global last_random
    last_random = (a * last_random + c) % m
    return last_random / m  # Retorna um número entre 0 e 1
