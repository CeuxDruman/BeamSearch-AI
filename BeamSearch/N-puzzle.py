# N-Puzzle from Artificial Intelligence Subject

# Important data:
#   N       -> Number of pieces

from random import shuffle
from math import sqrt
from copy import deepcopy
import random
import sys
import búsqueda_en_haz as BS
import búsqueda_en_haz_con_vuelta_atrás as BSBT
import búsqueda_en_haz_con_discrepancias as BSD
import búsqueda_en_haz_backtracking as BSBack # ASDASDASDASDASDASDASD ELIMINAR !!!!!!!

sys.setrecursionlimit(10000)

def neighbours(state):

    result = []
    num_Casillas = len(state)
    M = sqrt(num_Casillas)
    tablero = [] # Tablero dividido en filas
    tablero.append([]) # Le metemos la primera fila vacía
    num_row = 0
    num_col = 0
    zero_row = -1
    zero_col = -1

    # Dividimos el tablero en filas

    for num in state:                   # por cada casilla
        if num_col == M:                # si el último elemento que se metió estaba al final de una fila
            tablero.append([])          # creamos la fila siguiente
            num_row = num_row + 1       # aumentamos el contador de filas
            num_col = 0                 # ponemos el contador de columnas a 0 (la primera)
        tablero[num_row].append(num)    # Metemos la siguiente pieza en la casilla que le corresponde
        if(num == 0):
            zero_row = num_row
            zero_col = num_col
        num_col = num_col + 1           # aumentamos el contador de columnas (para que la siguiente pieza vaya en la casila de su derecha)

    # Detectamos los vecinos del estado actual

    posCasillaVacia = state.index(0)

    if(not zero_row-1< 0):
        #print("Vecino de arriba")
        vecino1 = (zero_col,zero_row-1)               # Vecino de arriba
        state1 = deepcopy(state)
        pieza1 = tablero[vecino1[1]][vecino1[0]]
        posPieza1EnState = state.index(pieza1)
        state1[posPieza1EnState] = 0
        state1[posCasillaVacia] = pieza1
        result.append(state1)
        #print(state1)
    if(not zero_col+1 > M-1):
        #print("Vecino a la derecha")
        vecino2 = (zero_col+1,zero_row)               # Vecino a la derecha
        state2 = deepcopy(state)
        pieza2 = tablero[vecino2[1]][vecino2[0]]
        posPieza2EnState = state.index(pieza2)
        state2[posPieza2EnState] = 0
        state2[posCasillaVacia] = pieza2
        result.append(state2)
        #print(state2)
    if(not zero_row+1 > M-1):
        #print("Vecino de abajo")
        vecino3 = (zero_col,zero_row+1)               # Vecino de abajo
        state3 = deepcopy(state)
        pieza3 = tablero[vecino3[1]][vecino3[0]]
        posPieza3EnState = state.index(pieza3)
        state3[posPieza3EnState] = 0
        state3[posCasillaVacia] = pieza3
        result.append(state3)
        #print(state3)
    if(not zero_col-1< 0):
        #print("Vecino a izquierda")
        vecino4 = (zero_col-1,zero_row)               # Vecino de la izquierda
        state4 = deepcopy(state)
        pieza4 = tablero[vecino4[1]][vecino4[0]]
        posPieza4EnState = state.index(pieza4)
        state4[posPieza4EnState] = 0
        state4[posCasillaVacia] = pieza4
        result.append(state4)
        #print(state4)

    return result

def heuristic(state):

    num_col = 1
    num_row = 1
    M = sqrt(len(state))
    result = 0
    initial_state = deepcopy(state)
    initial_state.sort()

    #print(state)
    #print(initial_state)

    # Debemos sacar la suma de fila+columna de la pieza en el ESTADO ACTUAL y restarle el mismo cálculo en el ESTADO INICIAL (en valor absoluto)

    for num in state: # ESTADO ACTUAL  # por cada casilla

        current_res = 1
        initial_res = 1

        if num_col == M+1:  # si el último elemento que se metió estaba al final de una fila
            num_row = num_row + 1  # aumentamos el contador de filas
            num_col = 1  # ponemos el contador de columnas a 0 (la primera)

        #current_res = num_row + num_col
        #print("CURRENT: El %s está en fila %s columna %s" % (num, num_row, num_col))

        initial_num_col = 1
        initial_num_row = 1
        for initial_num in initial_state: # ESTADO INICIAL
            if initial_num_col == M+1:
                initial_num_row = initial_num_row + 1
                initial_num_col = 1

            if(initial_num == num):
                #initial_res = initial_num_row + initial_num_col
                #print("INITIAL: El %s está en fila %s columna %s" % (initial_num, initial_num_row, initial_num_col))
                break

            initial_num_col = initial_num_col + 1

        result = result + abs(num_row - initial_num_row) + abs(num_col - initial_num_col)

        #if(result > 0):
        #    print("El número %s estaba en la fila %s y columna %s, mientras que en initial_state estaba en fila %s columna %s" % (num, num_row, num_col, initial_num_row, initial_num_col))


        num_col = num_col + 1  # aumentamos el contador de columnas (para que la siguiente pieza vaya en la casila de su derecha)

    #result = zero_row + zero_col
    return result

def N_Puzzle(N):

    num_Piezas = N
    num_Casillas = N + 1
    estado_final = []#[a for a in range(num_Casillas)]
    estado_inicial = []#[a for a in range(num_Casillas)]
    #shuffle(estado_inicial)

    #random.seed(3452168)
    random.seed(123456)
    
    for a in range(num_Casillas):
        rand_num = random.randrange(num_Casillas)
        while rand_num in estado_inicial:
            rand_num = random.randrange(num_Casillas)
        estado_inicial.append(rand_num)

    estado_final = deepcopy(estado_inicial)
    estado_final.sort()

    print("estado_inicial: %s" % (estado_inicial))
    print("estado_final: %s" % (estado_final))

    BS.heuristic = heuristic
    BS.neighbours = neighbours

    #return BS.busqueda_en_haz(1, estado_inicial, num_Casillas, estado_final)
    #return BS.busqueda_en_haz(1, estado_inicial, 1000, estado_final) # Error out of bound
    #return BS.busqueda_en_haz(8, estado_inicial, 1000, estado_final) # Sigue sin encontrar nada, se queda in memoria
    #return BS.busqueda_en_haz(4, estado_inicial, 2000, estado_final)
    #return BS.busqueda_en_haz(4, [2,1,0,3,4,5,6,7,8], 2000, estado_final) # Sigue sin encontrar nada, se queda in memoria
    #return BS.busqueda_en_haz(4, [1,2,0,3,4,5,6,7,8], 2000, estado_final) # Funciona sin problemas
    #return BS.busqueda_en_haz(4, [1,2,5,3,4,0,6,7,8], 2000, estado_final) # Funciona sin problemas

    #return BS.busqueda_en_haz(4, [3,2,5,1,4,0,6,7,8], 2000, estado_final) # Ya no encuentra nada
    #return BS.busqueda_en_haz(1, [3,2,5,1,4,0,6,7,8], 2000, estado_final) # Ya no encuentra nada

    #return BS.busqueda_en_haz(3, [2,1,0,3,4,5,6,7,8], 30, estado_final)
    #return BS.busqueda_en_haz(1, [2,1,0,3,4,5,6,7,8], 1, estado_final)
    #return BS.busqueda_en_haz(1, estado_inicial, 2000, estado_final)
    #return BS.busqueda_en_haz(2, estado_inicial, 2000, estado_final)

    BSBT.heuristic = heuristic
    BSBT.neighbours = neighbours

    #return BSBT.busqueda_en_haz_backtracking(4, [3,2,5,1,4,0,6,7,8], 2000, estado_final)
    #return BSBT.busqueda_en_haz_backtracking(1, estado_inicial, 500, estado_final)

    BSBack.heuristic = heuristic # ASDASDASDASDASDASDASD ELIMINAR !!!!!!!
    BSBack.neighbours = neighbours # ASDASDASDASDASDASDASD ELIMINAR !!!!!!!

    # return BSBack.busqueda_en_haz(1, estado_inicial, 2000, estado_final) # ASDASDASDASDASDASDASD ELIMINAR !!!!!!!

    BSD.heuristic = heuristic
    BSD.neighbours = neighbours

    return BSD.BULB([2,4,8,7,3,5,1,6,0], estado_final, 5, 150)



#print(N_Puzzle(3))
print(N_Puzzle(8))
#print(N_Puzzle(15))
#print(N_Puzzle(24))
#print(N_Puzzle(99))
#N_Puzzle(8)

#print(neighbours([0,1,2,3,4,5,6,7,8]))
#print(heuristic([2,1,0,3,4,8,6,7,5]))
#print(heuristic([0, 3, 6, 1, 4, 8, 2, 5, 7]))
#print(heuristic([0, 2, 1, 3, 4, 5, 6, 7, 8]))
#print(heuristic([0, 3, 2, 1, 4, 5, 6, 7, 8])) # 4
#print(heuristic([7,4,6,2,1,8,0,3,5])) #Debe salir 18
#print(heuristic([5,6,2,1,3,7,8,0,4])) #Debe salir 18

