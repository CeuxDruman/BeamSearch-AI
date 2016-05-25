# N-Puzzle from Artificial Intelligence Subject

# Important data:
#   N       -> Number of pieces

from random import shuffle
from math import sqrt
from copy import deepcopy

def N_Puzzle(N):

    num_Piezas = N
    num_Casillas = N + 1
    estado_final = [a for a in range(num_Casillas)]
    estado_inicial = [a for a in range(num_Casillas)]
    shuffle(estado_inicial)

    print("estado_final: %s" % (estado_final))
    print("estado_inicial: %s" % (estado_inicial))

    return busqueda_en_haz2(1, estado_inicial, num_Casillas, estado_final)
    #return busqueda_en_haz2(3, [2,1,0,3,4,5,6,7,8], 30, estado_final)
    #return busqueda_en_haz2(1, [2,1,0,3,4,5,6,7,8], 1, estado_final)


def busqueda_en_haz2(B, initial_state, memory, goal_state):
    # Initialization
    g = 0  # Cost
    hash_table = []  # Memory
    BEAM = [initial_state]

    # Main loop
    while len(BEAM) != 0:  # loop until the BEAM contains no nodes
        SET = []  # the empty set

        print("BEAM: %s" % (BEAM))

        # Generate the SET nodes
        for state in BEAM:
            #print("neighbours: %s" % (neighbours(state)))
            contadoor = 0
            for successor in neighbours(state):
                #print("Sucesor %s: %s" % (contadoor, successor))
                if successor == goal_state:
                    g = g + 1
                    return g
                if successor not in SET:
                    #print("pre-SET: %s" % (SET))
                    SET.append(successor)
                    #print("añadido")
                    #print("post-SET: %s" % (SET))
                contadoor = contadoor + 1

        print("SET sin ordenar: %s" % (SET))

        ### Order the SET nodes ascending by their Heur.

        # OPTION 1
        SETOrdered = []

        count = 0
        currentState = SET[count]

        #while count < len(SET):
        for a in SET: # Recorremos una vez el SET por cada elemento que contenga

           # Filtramos primero para asegurarnos de que el estado recorrido no esté ya en la lista ordenada
           cS = deepcopy(currentState)
           for eachElement in SET:
               if(cS not in SETOrdered):
                   break
               else:
                    cS = deepcopy(eachElement)
           currentState = deepcopy(cS)

           # Ahora cogemos el mejor de esta iteración, sin tener en cuenta los ya cogidos en iteraciones anteriores

           #currentState = SET[count]
           for state in SET:
               if (heuristic(state) < heuristic(currentState)) and (state not in SETOrdered):
                   #print("Supuestamente %s no está en %s" % (state, SETOrdered))
                   currentState = deepcopy(state)
           print("currentState: %s (Heur: %s)" % (currentState,heuristic(currentState)))
           SETOrdered.append(currentState)
           #count = count + 1

        SET = SETOrdered

        # OPTION 2
        #SET.sort(key=lambda state: state.heuristic, reverse=False)

        print("SET ordenado: %s" % (SET))

        BEAM = []  # the empty set
        g = g + 1

        # Fill the BEAM for the next loop
        while len(SET) != 0 and B > len(BEAM):
            count = 0
            while count < B:
                #print(SET)
                if(count > len(SET)-1):
                    break
                state = SET.pop(count)
                BEAM.append(state)
                count = count + 1

        for state in BEAM:
            if state not in hash_table:
                print("HT: %s MM: %s" % (len(hash_table), memory))
                if len(hash_table) >= memory:
                    return float('inf')
                hash_table.append(state)

    return g

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

    num_col = 0
    num_row = 0
    zero_col = -1
    zero_row = -1
    M = sqrt(len(state))

    for num in state:  # por cada casilla
        if num_col == M:  # si el último elemento que se metió estaba al final de una fila
            num_row = num_row + 1  # aumentamos el contador de filas
            num_col = 0  # ponemos el contador de columnas a 0 (la primera)
        if (num == 0):
            zero_row = num_row
            zero_col = num_col
            break
        num_col = num_col + 1  # aumentamos el contador de columnas (para que la siguiente pieza vaya en la casila de su derecha)

    result = zero_row + zero_col
    return result

print(N_Puzzle(8))
#print(N_Puzzle(15))
#print(N_Puzzle(24))
#print(N_Puzzle(99))
#N_Puzzle(8)

#print(neighbours([0,1,2,3,4,5,6,7,8]))
#print(heuristic([0,1,2,3,4,5,6,7,8]))
