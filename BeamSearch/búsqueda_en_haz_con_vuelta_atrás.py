# BeamSearch w/ Backtracking from Artificial Intelligence Subject

# Important data:
#   h           -> Heuristic function
#   B           -> The number of nodes that are stored at each level of the Breadth-First Search.
#   BEAM        -> Store the nodes that are to be expanded in the next loop of the algorithm.
#   hash_table  -> Store nodes that have been visited. (Memory)
#   g           -> Used to keep track of the depth of the search, which is the cost of reaching a node at that level.
#   SET         -> Set of successor nodes

from math import sqrt
from copy import deepcopy

global heuristic
global neighbours

# def BULB(initial_state, heuristic, B):
#
#     # Initialization
#     discrepancies = 0
#     g = 0;
#     hash_table = []
#
#     while True:
#         pathlength = BULBprobe(0, discrepancies, heuristic, B)
#         if pathlength < float('inf'):
#             return pathlength
#         discrepancies = discrepancies + 1
#
# def BULBprobe(depth, discrepancies, heuristic, B):
#
#     [SLICE, value, index] = nextSlice(depth, 0, heuristic, B)
#
#     if value >= 0:
#         return value
#
#     if discrepancies == 0:
#
#         if SLICE is []:
#             return float('inf')
#         pathlenght = BULBprobe(depth+1, 0, heuristic, B)
#         for s in SLICE:
#             hash_table.remove(s)
#         return pathlenght
#
#     else:
#
#         if SLICE is not []:
#             for s in SLICE:
#                 hash_table.remove(s)
#         while True:
#             [SLICE, value, index] = nextSlice(depth, index, heuristic, B)
#             if value >= 0:
#                 if value < float('inf'):
#                     return value
#                 else:
#                     break
#             if SLICE is []:
#                 continue
#             pathlenght = BULBprobe(depth+1, discrepancies-1, heuristic, B)
#             for s in SLICE:
#                 hash_table.remove(s)
#             if pathlenght < float('inf'):
#                 return pathlenght
#         [SLICE, value, index] = nextSlice(depth, 0, heuristic, B)
#         if value >= 0:
#             return value
#         if SLICE is []:
#             return float('inf')
#         pathlenght = BULBprobe(depth+1, discrepancies, heuristic, B)
#         for s in SLICE:
#             hash_table.remove(s)
#         return pathlenght
#
# def nextSlice(depth, index, heuristic, B):
#
#     currentlayer = # g() obtener el nivel del estado: Sacar de la memoria el bloque que está en el nivel s # Linea 43: depth + 1

def busqueda_en_haz_backtracking(B, initial_state, memory, goal_state):
    # Initialization
    g = 0  # Cost
    hash_table = []  # Memory
    BEAM = [initial_state]
    leafBacktracking = False
    SET = []
    nBacks = 0
    level = 0
    hash_levels = []

    hash_table.append(initial_state)
    hash_levels.append(level)

    # Main loop
    while len(BEAM) != 0:  # loop until the BEAM contains no nodes
        #print("Otra vez")
        print("-----------------")
        level = level + 1
        #SET = []  # the empty set

        # print("BEAM: %s" % (BEAM))

        # Generate the SET nodes

        if not leafBacktracking:

            SETtemp = []

            for state in BEAM:
                # print("neighbours: %s" % (neighbours(state)))
                #count1 = 0
                for successor in neighbours(state):
                    # print("Sucesor %s: %s" % (contadoor, successor))
                    if successor not in hash_table:
                        if successor == goal_state:
                            g = g + 1
                            return g
                        if successor not in SETtemp:
                            # print("pre-SET: %s" % (SET))
                            SETtemp.append(successor)
                            # print("añadido")
                            # print("post-SET: %s" % (SET))
                    #count1 = count1 + 1

            # print("SET sin ordenar: %s" % (SET))

            if len(SETtemp) == 0:

                # Comprobamos que hay más hojas para recorrer en su nivel (hermanos)
                hayMasElementos = False
                for s in SET:
                    if s not in hash_table:
                        hayMasElementos = True

                if hayMasElementos:
                    print("------------------------------- BACKTRACKING HACIA HERMANO ----------------------------------")
                    print("SET: %s" % (SET))
                    leafBacktracking = True
                    nBacks = 0
                    level = level - 2
                    continue
                else:
                    print("------------------------------- BACKTRACKING HACIA ABUELO ----------------------------------")
                    nBacks = nBacks + 1
                    BEAM = []
                    count2 = 1
                    index = B*nBacks
                    while count2 <= B:
                        BEAM.append(hash_table[len(hash_table)-1-index])
                        count2 = count2 + 1
                        index = index - 1
                    print("BEAM: %s" % (BEAM))
                    #if nBacks == 1:
                    level = level - 2
                    #else:
                    #    level = level - 2
                    continue
            else:
                nBacks = 0
                SET = deepcopy(SETtemp)

            ### Order the SET nodes ascending by their Heur.

            # OPTION 1
            SETOrdered = []

            #count3 = 0
            currentState = SET[0]

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
                print("sucessor: %s (Heur: %s)" % (currentState, heuristic(currentState)))
                SETOrdered.append(currentState)
                # count = count + 1

            #print("-----------------")

            SET = SETOrdered

        # print("SET ordenado: %s" % (SET))

        BEAM = []  # the empty set
        g = g + 1

        # Fill the BEAM for the next loop
        while len(SET) != 0 and B > len(BEAM):
            count4 = 0
            while count4 < B:
                # print(SET)
                if (count4 > len(SET) - 1):
                    break
                state = SET.pop(0)
                if leafBacktracking:
                    if state not in hash_table:
                        BEAM.append(state)
                else:
                    BEAM.append(state)
                count4 = count4 + 1

        statesToRemove = 0
        print("BEAM: %s" % (BEAM))

        for state in BEAM:
            if state not in hash_table:
                print("HT: %s MM: %s" % (len(hash_table), memory))
                if len(hash_table) >= memory:
                    #print("hash_table: %s" % (hash_table))
                    #print("hash_levels: %s" % (hash_levels))

                    return float('inf')

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
                print("A memoria: %s" % (state))
                hash_levels.append(level)
                print("level: %s" % (level))
                statesToRemove = statesToRemove + 1

        leafBacktracking = False

        #if len(BEAM) == 0:
        #    print("------------------------------- BACKTRACKING HACIA PADRE ----------------------------------")
        #    nBacks = nBacks + 1
        #    BEAM = []
        #    count5 = 1
        #    index = B*nBacks
        #    while count5 <= B:
        #        BEAM.append(hash_table[len(hash_table)-1-index])
        #        count5 = count5 + 1
        #        index = index - 1

    
    return "Hemos llegado al final del árbol. Coste: %s" % (g)
