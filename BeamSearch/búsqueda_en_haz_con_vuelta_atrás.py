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
#     currentlayer =

def busqueda_en_haz_backtracking(B, initial_state, memory, goal_state):
    # Initialization
    g = 0  # Cost
    hash_table = []  # Memory
    hash_table.append(initial_state)
    BEAM = [initial_state]
    backtracking = False
    SET = []

    # Main loop
    while len(BEAM) != 0:  # loop until the BEAM contains no nodes
        print("Otra vez")
        #SET = []  # the empty set

        # print("BEAM: %s" % (BEAM))

        # Generate the SET nodes

        if not backtracking:

            SETtemp = []

            for state in BEAM:
                # print("neighbours: %s" % (neighbours(state)))
                contadoor = 0
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
                    contadoor = contadoor + 1

            # print("SET sin ordenar: %s" % (SET))

            if len(SETtemp) == 0:
                print("SET: %s" % (SET))
                backtracking = True
                continue
            else:
                SET = deepcopy(SETtemp)

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
                if backtracking:
                    if state not in hash_table:
                        BEAM.append(state)
                else:
                    BEAM.append(state)
                count = count + 1

        for state in BEAM:
            if state not in hash_table:
                print("HT: %s MM: %s" % (len(hash_table), memory))
                if len(hash_table) >= memory:
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

        backtracking = False

    
    return "Hemos llegado al final del árbol. Coste: %s" % (g)
