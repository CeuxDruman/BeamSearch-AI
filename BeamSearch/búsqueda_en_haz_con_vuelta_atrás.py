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

def busqueda_en_haz_backtracking(B, initial_state, memory, goal_state):
    # Initialization
    g = 0  # Cost
    hash_table = []  # Memory
    hash_levels = [] # Nivel en el que se encuentra cada elemento de memoria (hash_table)
    hash_level_index = [] # Posici�n del nivel que toca explorar
    BEAM = [initial_state]
    #leafBacktracking = False
    #SET = []
    nBacks = 0
    level = 0
    #backtrackingStop = False
    backtrackingCount = 10

    hash_table.append(initial_state)
    hash_levels.append(level)
    hash_level_index.append(0)

    # Main loop
    while len(BEAM) != 0:  # loop until the BEAM contains no nodes
        print("-----------------")
        level = level + 1
        if hash_levels[len(hash_levels)-1] + 1 == level:
            hash_level_index.append(0)
        SET = []  # the empty set

        #if backtrackingStop:
        #    if backtrackingCount == 0:
        #        return "Ha hecho backtracking"
        #    backtrackingCount = backtrackingCount - 1

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
                        # print("a�adido")
                        # print("post-SET: %s" % (SET))
                contadoor = contadoor + 1

        # print("SET sin ordenar: %s" % (SET))

        if len(SET) != 0:
            ### Order the SET nodes ascending by their Heur.

            SETOrdered = []

            #count = 0
            currentState = SET[0]

            # while count < len(SET):
            for a in SET:  # Recorremos una vez el SET por cada elemento que contenga

                # Filtramos primero para asegurarnos de que el estado recorrido no est� ya en la lista ordenada
                cS = deepcopy(currentState)
                for eachElement in SET:
                    if (cS not in SETOrdered):
                        break
                    else:
                        cS = deepcopy(eachElement)
                currentState = deepcopy(cS)

                # Ahora cogemos el mejor de esta iteraci�n, sin tener en cuenta los ya cogidos en iteraciones anteriores

                # currentState = SET[count]
                for state in SET:
                    if (heuristic(state) < heuristic(currentState)) and (state not in SETOrdered):
                        # print("Supuestamente %s no est� en %s" % (state, SETOrdered))
                        currentState = deepcopy(state)
                print("sucessor: %s (Heur: %s)" % (currentState, heuristic(currentState)))
                SETOrdered.append(currentState)
                # count = count + 1



            SET = SETOrdered

        # Filter the nodes that have been already visited on this level
        SETToFilter = deepcopy(SET)
        print("hash_level_index[level]: %s" % (hash_level_index[level]))
        count3 = 0
        print("SET pre-filter: %s" % (SET))
        for node in SETToFilter:
            if count3 < hash_level_index[level]:
                print("Already visited: %s" % (SET.pop(0)))
            count3 = count3 + 1

        if len(SET) == 0: # SI LLEGAMOS A UNA HOJA DEL �RBOL (No hay sucesores)
            #backtrackingStop = True
            print("\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/ Backtracking \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
            print("nivel: %s" % (level))
            print("hash_table size: %s" % (len(hash_table)))
            print("hash_levels size: %s" % (len(hash_levels)))

            # Borramos los bloques anteriores
            nivel = level-1
            #for nvl in hash_levels:
            #    if nvl == nivel:
            #        hash_table.pop(hash_levels.index(nvl)) # Borramos de memoria todos los bloques anteriores
            #hash_levels = list(filter((nvl).__ne__, hash_levels)) # Borramos todos los elementos de este nivel

            count5 = len(hash_levels) - 1
            while count5 >= 0:
                if hash_levels[count5] == nivel:
                    hash_table.pop(count5)
                count5 = count5 - 1
            hash_levels = list(filter((nivel).__ne__, hash_levels)) # Borramos todos los elementos de este nivel

            level = level - 2 # Volvemos al nivel del Padre (BEAM)

            # Volvemos al BEAM anterior
            BEAM = []
            count4 = 0
            for lvl in hash_levels:
                if lvl == level:
                    BEAM.append(hash_table[count4])
                count4 = count4 + 1

            print("BEAM tras Backtracking: %s" % (BEAM))

            hash_level_index[level+1] = hash_level_index[level+1] + B

            hash_level_index[level + 2] = 0

            continue

        # print("SET ordenado: %s" % (SET))

        BEAM = []  # the empty set
        g = g + 1

        #if hash_levels[len(hash_levels)-1] + 1 == level:
        #    hash_level_index.append(0)

        

        # Fill the BEAM for the next loop
        while len(SET) != 0 and B > len(BEAM):
            state = SET.pop(0)
            if state not in hash_table:
                #print("HT: %s MM: %s" % (len(hash_table), memory))
                if len(hash_table) >= memory:
                    #backtrackingStop = True
                    print("\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/ Backtracking (memory) \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
                    print("nivel: %s" % (level))
                    print("hash_table size: %s" % (len(hash_table)))
                    print("hash_levels size: %s" % (len(hash_levels)))

                    # Borramos los bloques de este nivel
                    nivel = level
                    #count5 = 0
                    #for nvl in hash_levels:
                    #    if nvl == nivel:
                    #        hash_table.pop(count5) # Borramos de memoria todos los bloques anteriores
                    #    count5 = count5 + 1
                    count5 = len(hash_levels) - 1
                    while count5 >= 0:
                        if hash_levels[count5] == nivel:
                            hash_table.pop(count5)
                        count5 = count5 - 1

                    hash_levels = list(filter((nivel).__ne__, hash_levels)) # Borramos todos los elementos de este nivel

                    # Borramos los bloques anteriores
                    #nivel = level-1
                    #for nvl in hash_levels:
                    #    if nvl == nivel:
                    #        hash_table.pop(hash_levels.index(nvl)) # Borramos de memoria todos los bloques anteriores
                    #hash_levels = list(filter((nvl).__ne__, hash_levels)) # Borramos todos los elementos de este nivel

                    level = level - 2 # Volvemos al nivel del Padre (BEAM)

                    # Volvemos al BEAM anterior
                    BEAM = []
                    count4 = 0
                    for lvl in hash_levels:
                        if lvl == level:
                            BEAM.append(hash_table[count4])
                        count4 = count4 + 1

                    print("BEAM tras Backtracking: %s" % (BEAM))

                    hash_level_index[level+1] = hash_level_index[level+1] + B

                    hash_level_index[level + 2] = 0

                    print("post-hash_table size: %s" % (len(hash_table)))
                    print("post-hash_levels size: %s" % (len(hash_levels)))

                    continue

                    #return float('inf')

                    # para averiguar si hemos implementado bien el que no se tomen en cuenta nodos ya explorados
                    # lst = hash_table
                    # lst2 = []
                    # for key in lst:
                    #     if key not in lst2:
                    #         lst2.append(key)
                    #     else:
                    #         return "Acabó: %s" % (key)
                    # return "No se repite nada"

                hash_table.append(state)
                #print("A memoria: %s" % (state))

                BEAM.append(state)
                hash_levels.append(level)
                print("HT: %s MM: %s" % (len(hash_table), memory))
        print("BEAM: %s" % (BEAM))
        print("level: %s" % (level))


    return "No se ha encontrado solución. Coste: %s" % (g)

#import random

#for i in range(10): print(random.randrange(100)) # Distintos

#random.seed(365273) # Cambiar semilla para 15 instancias que para 30, 100, etc...
                    # No cambiar semilla de un algoritmo a otro de b�squeda en haz