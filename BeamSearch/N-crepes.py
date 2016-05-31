# N-Crepes from Artificial Intelligence Subject

# Important data:
#   N       -> Number of crepes

from random import shuffle
from math import sqrt
from copy import deepcopy

def N_Crepes(N):

    num_Crepes = N
    estado_final = [a for a in range(1,num_Crepes+1)]
    estado_inicial = [a for a in range(1,num_Crepes+1)]
    shuffle(estado_inicial)

    print("estado_final: %s" % (estado_final))
    print("estado_inicial: %s" % (estado_inicial))

    return busqueda_en_haz3(1, estado_inicial, num_Crepes, estado_final)
    #return busqueda_en_haz3(1, [1,2,3,4,5,6,7,8,9], num_Crepes, estado_final)
    #return busqueda_en_haz3(1, [1,2,3,4,5,6,7,8,9], num_Crepes, estado_final)


def busqueda_en_haz3(B, initial_state, memory, goal_state):
    # Initialization
    g = 0  # Cost
    hash_table = []  # Memory
    BEAM = [initial_state]

    # Main loop
    while len(BEAM) != 0:  # loop until the BEAM contains no nodes
        SET = []  # the empty set

        #print("BEAM: %s" % (BEAM))

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

        #print("SET sin ordenar: %s" % (SET))

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
        
        print("-----------------")

        SET = SETOrdered

        # OPTION 2
        #SET.sort(key=lambda state: state.heuristic, reverse=False)

        #print("SET ordenado: %s" % (SET))

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

print("Result: %s" % (N_Crepes(9)))
#print("Result: %s" % (N_Crepes(30)))
#print("Result: %s" % (N_Crepes(40)))
#print("Result: %s" % (N_Crepes(50)))
#print("Result: %s" % (N_Crepes(60)))
#print("Result: %s" % (N_Crepes(100)))

#print(neighbours([3,2,5,1,6,4]))
#print(heuristic([1,2,3,4,5,6,7,8,9]))
#print(heuristic([3,2,5,1,6,4]))
#print(heuristic([3,2,5,1,4,6]))
