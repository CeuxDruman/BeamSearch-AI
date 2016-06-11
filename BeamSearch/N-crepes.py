# N-Crepes from Artificial Intelligence Subject

# Important data:
#   N       -> Number of crepes

from random import shuffle
from math import sqrt
from copy import deepcopy
import random
import búsqueda_en_haz as BS
import búsqueda_en_haz_con_vuelta_atrás as BSBT
import búsqueda_en_haz_con_discrepancias as BSD

def neighbours(state):

    result = []
    c = 2

    for a in state:

        k = c

        if(k == len(state)+1):
            break

        copiedState = deepcopy(state)
        crepesToInvest = []
        #counter = 0

        # Primero obtenemos los k crepes de encima de la pila
        for crepe in state:
            if(k == 0):
                break
            crepesToInvest.append(crepe)
            copiedState.pop(0)
            k = k - 1
            #counter = counter + 1

        # Invertimos esos k crepes
        #investedCrepes = crepesToInvest.reverse()

        # Los ponemos de nuevo encima de la pila en orden invertido
        for investedCrepe in crepesToInvest:
            copiedState.insert(0, investedCrepe)

        result.append(copiedState)

        c = c + 1

    return result

def heuristic(state):

    h = 0
    plateValue = len(state)+1
    #print(len(state))

    counter = 0
    for crepe in state:
        if(counter+1 == len(state)):
            if(crepe != plateValue-1):
                h = h + 1
            #print("Plato: %s Plato+1: %s Heur: %s" % (crepe, plateValue, h))
        else:
            if(crepe-1 != state[counter+1] and crepe+1 != state[counter+1]):
                h = h + 1
            #print("Plato: %s Plato+1: %s Heur: %s" % (crepe, state[counter+1], h))
        counter = counter + 1

    return h

def N_Crepes(N):

    num_Crepes = N
    #estado_final = [a for a in range(1,num_Crepes+1)]
    #estado_inicial = [a for a in range(1,num_Crepes+1)]
    #shuffle(estado_inicial)

    estado_final = []
    estado_inicial = []

    random.seed(6452357)
    
    for a in range(1,num_Crepes+1):
        rand_num = random.randrange(1,num_Crepes+1)
        while rand_num in estado_inicial:
            rand_num = random.randrange(1,num_Crepes+1)
        estado_inicial.append(rand_num)

    estado_final = deepcopy(estado_inicial)
    estado_final.sort()

    print("estado_final: %s" % (estado_final))
    print("estado_inicial: %s" % (estado_inicial))

    BS.heuristic = heuristic
    BS.neighbours = neighbours

    BSBT.heuristic = heuristic
    BSBT.neighbours = neighbours

    #return BS.busqueda_en_haz(1, estado_inicial, num_Crepes, estado_final)
    #return BS.busqueda_en_haz(2, estado_inicial, num_Crepes, estado_final) #30 # Se queda sin memoria
    #return BS.busqueda_en_haz(2, estado_inicial, 100, estado_final) #30 # Se estanca en Heur 5/6
    #return BS.busqueda_en_haz(3, estado_inicial, 100, estado_final) #30 # FUNCIONA: Result: 35 justo antes de quedarse sin memoria (99 de 100)

    #return BS.busqueda_en_haz(1, [1,2,3,4,5,6,7,8,9], num_Crepes, estado_final)
    #return BS.busqueda_en_haz(1, [1,2,3,4,5,6,7,8,9], num_Crepes, estado_final)

    #return BS.busqueda_en_haz(1, estado_inicial, 100, estado_final) # PERFECTO: Acaba usando 35 de memoria con coste: 36

    return BSBT.busqueda_en_haz_backtracking(1, [2,4,3,1], 100, estado_final)

print("Result: %s" % (N_Crepes(4)))
#print("Result: %s" % (N_Crepes(9)))
#print("Result: %s" % (N_Crepes(30)))
#print("Result: %s" % (N_Crepes(40)))
#print("Result: %s" % (N_Crepes(50)))
#print("Result: %s" % (N_Crepes(60)))
#print("Result: %s" % (N_Crepes(100)))

#print(neighbours([3,2,5,1,6,4]))
#print(heuristic([1,2,3,4,5,6,7,8,9]))
#print(heuristic([3,2,5,1,6,4]))
#print(heuristic([3,2,5,1,4,6]))
