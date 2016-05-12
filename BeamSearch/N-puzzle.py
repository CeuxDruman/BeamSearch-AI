# N-Puzzle from Artificial Intelligence Subject

# Important data:
#   N       -> Number of pieces

from random import shuffle

def N_Puzzle(N):

    num_Piezas = N
    num_Casillas = N + 1
    estado_final = [a for a in range(num_Casillas)]
    estado_inicial = [a for a in range(num_Casillas)]
    shuffle(estado_inicial)

    #print(estado_final)
    #print(estado_inicial)

    return 0

N_Puzzle(10)