# BeamSearch from Artificial Intelligence Subject

# Important data:
#   h           -> Heuristic function
#   B           -> The number of nodes that are stored at each level of the Breadth-First Search.
#   BEAM        -> Store the nodes that are to be expanded in the next loop of the algorithm.
#   hash_table  -> Store nodes that have been visited. (Memory)
#   g           -> Used to keep track of the depth of the search, which is the cost of reaching a node at that level.
#   SET         -> Set of successor nodes

# How it works:
# - Each time through the main loop of the algorithm, Beam Search adds all of the nodes connected to the nodes in the BEAM to its SET of successor nodes and then adds the B nodes with the best heuristic values from the SET to the BEAM and the hash table.
# - Note that a node that is already in the hash table is not added to the BEAM because a shorter path to that node has already been found.
# - This process continues until the goal node is found, the hash table becomes full (indicating that the memory available has been exhausted), or the BEAM is empty after the main loop has completed (indicating a dead end in the search).

from math import sqrt
from copy import deepcopy

global heuristic
global neighbours

def busqueda_en_haz(B, initial_state, memory, goal_state):
    # Initialization
    g = 0  # Cost
    hash_table = []  # Memory
    BEAM = [initial_state]

    # Main loop
    while len(BEAM) != 0:  # loop until the BEAM contains no nodes
        SET = []  # the empty set

        # print("BEAM: %s" % (BEAM))

        # Generate the SET nodes
        for state in BEAM:
            # print("neighbours: %s" % (neighbours(state)))
            contadoor = 0
            for successor in neighbours(state):
                # print("Sucesor %s: %s" % (contadoor, successor))
                if successor not in hash_table:
                    if successor == goal_state:
                        g = g + 1
                        return g
                    if successor not in SET:
                        # print("pre-SET: %s" % (SET))
                        SET.append(successor)
                        # print("añadido")
                        # print("post-SET: %s" % (SET))
                contadoor = contadoor + 1

        # print("SET sin ordenar: %s" % (SET))

        ### Order the SET nodes ascending by their Heur.

        # OPTION 1
        SETOrdered = []

        count = 0
        currentState = SET[count]

        # while count < len(SET):
        for a in SET:  # Recorremos una vez el SET por cada elemento que contenga

            # Filtramos primero para asegurarnos de que el estado recorrido no esté ya en la lista ordenada
            cS = deepcopy(currentState)
            for eachElement in SET:
                if (cS not in SETOrdered):
                    break
                else:
                    cS = deepcopy(eachElement)
            currentState = deepcopy(cS)

            # Ahora cogemos el mejor de esta iteración, sin tener en cuenta los ya cogidos en iteraciones anteriores

            # currentState = SET[count]
            for state in SET:
                if (heuristic(state) < heuristic(currentState)) and (state not in SETOrdered):
                    # print("Supuestamente %s no está en %s" % (state, SETOrdered))
                    currentState = deepcopy(state)
            print("currentState: %s (Heur: %s)" % (currentState, heuristic(currentState)))
            SETOrdered.append(currentState)
            # count = count + 1

        print("-----------------")

        SET = SETOrdered

        # OPTION 2
        # SET.sort(key=lambda state: state.heuristic, reverse=False)

        # print("SET ordenado: %s" % (SET))

        BEAM = []  # the empty set
        g = g + 1

        # Fill the BEAM for the next loop
        while len(SET) != 0 and B > len(BEAM):
            count = 0
            while count < B:
                # print(SET)
                if (count > len(SET) - 1):
                    break
                state = SET.pop(count)
                BEAM.append(state)
                count = count + 1

        for state in BEAM:
            if state not in hash_table:
                print("HT: %s MM: %s" % (len(hash_table), memory))
                if len(hash_table) >= memory:
                    # return float('inf')

                    # para averiguar si hemos implementado bien el que no se tomen en cuenta nodos ya explorados
                    lst = hash_table
                    lst2 = []
                    for key in lst:
                        if key not in lst2:
                            lst2.append(key)
                        else:
                            return "Acabó: %s" % (key)
                    return "No se repite nada"

                hash_table.append(state)

    return g

#import random

#for i in range(10): print(random.randrange(100)) # Distintos

#random.seed(365273) # Cambiar semilla para 15 instancias que para 30, 100, etc...
                    # No cambiar semilla de un algoritmo a otro de búsqueda en haz