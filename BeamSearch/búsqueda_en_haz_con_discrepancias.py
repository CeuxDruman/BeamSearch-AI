# BeamSearch w/ Discrepancies from Artificial Intelligence Subject
# Gastar la discrepancias lo antes posible

from copy import deepcopy

global heuristic
global neighbours

def BULB(initial_state, goal_state, B, memory):

    # Initialization
    discrepancies = 0
    state_level = 0;
    hash_table = [initial_state]
    hash_levels = [0]
    limitWhile = 1000000

    # print("Parada BULB 1")
    while limitWhile != 0:
        print("^^^^^^^^^^")
        print("Discrepancia: %s" % (discrepancies))
        # print("Parada BULB 2")
        pathlength = BULBprobe(0, discrepancies, B, hash_table, hash_levels, goal_state, memory)
        # print("Parada BULB 3")
        if pathlength < float('inf'):
            # print("Parada BULB 4")
            return pathlength
        discrepancies = discrepancies + 1
        limitWhile = limitWhile - 1
        # print("Parada BULB 5")

def BULBprobe(depth, discrepancies, B, hash_table, hash_levels, goal_state, memory):

    # print("Hash Table: %s" % (hash_table))
    # print("Hash Levels: %s" % (hash_levels))

    # print("Parada probe 1")
    [SLICE, value, index] = nextSlice(depth, 0, B, hash_table, hash_levels, goal_state, memory)

    # print("SLICE: %s" % (SLICE))
    # print("value: %s" % (value))
    # print("index: %s" % (index))

    if value >= 0:
        # print("Parada probe 2")
        return value

    if discrepancies == 0:
        # print("Parada probe 3")
        if SLICE is []:
            # print("Parada probe 4")
            return float('inf')
        # print("Parada probe 5")
        pathlenght = BULBprobe(depth+1, 0, B, hash_table, hash_levels, goal_state, memory)
        for s in SLICE:
            # print("Parada probe 6")
            if s in hash_table:
                # print("Parada probe 6.1")
                pos_in_hash_table = hash_table.index(s)
                # print("hash_table-preborrado-probe6.1: %s" % (hash_table))
                hash_table.remove(s)
                # print("hash_table-postborrado-probe6.1: %s" % (hash_table))
                # print("hash_levels-preborrado-probe6.2: %s" % (hash_levels))
                hash_levels.pop(pos_in_hash_table)
                # print("hash_levels-postborrado-probe6.3: %s" % (hash_levels))
            # print("Parada probe 7")
        return pathlenght
    else:
        # print("Parada probe 8")
        if SLICE is not []:
            # print("Parada probe 9")
            for s in SLICE:
                # print("Parada probe 10")
                if s in hash_table:
                    # print("Parada probe 10.1")
                    pos_in_hash_table = hash_table.index(s)
                    # print("hash_table-preborrado-probe10.1: %s" % (hash_table))
                    hash_table.remove(s)
                    # print("hash_table-postborrado-probe10.1: %s" % (hash_table))
                    # print("hash_levels-preborrado-probe10.2: %s" % (hash_levels))
                    hash_levels.pop(pos_in_hash_table)
                    # print("hash_levels-postborrado-probe10.3: %s" % (hash_levels))
                # print("Parada probe 11")
        while True:
            # print("Parada probe 12")
            [SLICE, value, index] = nextSlice(depth, index, B, hash_table, hash_levels, goal_state, memory)
            # print("Parada probe 13")
            if value >= 0:
                # print("Parada probe 14")
                if value < float('inf'):
                    # print("Parada probe 15")
                    return value
                else:
                    # print("Parada probe 16")
                    break
            if SLICE is []:
                # print("Parada probe 17")
                continue
            # print("Parada probe 18")
            pathlenght = BULBprobe(depth+1, discrepancies-1, B, hash_table, hash_levels, goal_state, memory)
            for s in SLICE:
                # print("Parada probe 19")
                if s in hash_table:
                    # print("Parada probe 19.1")
                    pos_in_hash_table = hash_table.index(s)
                    # print("hash_table-preborrado-probe19.1: %s" % (hash_table))
                    hash_table.remove(s)
                    # print("hash_table-postborrado-probe19.1: %s" % (hash_table))
                    # print("hash_levels-preborrado-probe19.2: %s" % (hash_levels))
                    hash_levels.pop(pos_in_hash_table)
                    # print("hash_levels-postborrado-probe19.3: %s" % (hash_levels))
                # print("Parada probe 20")
            if pathlenght < float('inf'):
                # print("Parada probe 21")
                return pathlenght
        # print("Parada probe 22")
        [SLICE, value, index] = nextSlice(depth, 0, B, hash_table, hash_levels, goal_state, memory)
        # print("Parada probe 23")
        if value >= 0:
            # print("Parada probe 24")
            return value
        if SLICE is []:
            # print("Parada probe 25")
            return float('inf')
        # print("Parada probe 26")
        pathlenght = BULBprobe(depth+1, discrepancies, B, hash_table, hash_levels, goal_state, memory)
        for s in SLICE:
            # print("Parada probe 26")
            if s in hash_table:
                # print("Parada probe 26.1")
                pos_in_hash_table = hash_table.index(s)
                # print("hash_table-preborrado-probe26.1: %s" % (hash_table))
                hash_table.remove(s)
                # print("hash_table-postborrado-probe26.1: %s" % (hash_table))
                # print("hash_levels-preborrado-probe26.2: %s" % (hash_levels))
                hash_levels.pop(pos_in_hash_table)
                # print("hash_levels-postborrado-probe26.3: %s" % (hash_levels))
            # print("Parada probe 27")
        return pathlenght

def nextSlice(depth, index, B, hash_table, hash_levels, goal_state, memory):

    ## currentlayer := {s in hash_table | g(s) = depth}

    currentlayer = []
    pos_in_list = 0

    # g() obtener el nivel del estado: Sacar de la memoria el bloque que está en el nivel s
    for i in hash_levels:
        if i == depth:
            # print("pos_in_list: %s" % (pos_in_list))
            # print("hash_table: %s" % (hash_table))
            # print("hash_levels: %s" % (hash_levels))
            currentlayer.append(hash_table[pos_in_list])
        pos_in_list = pos_in_list + 1


    SUCCS = generateNewSuccessor(currentlayer, hash_table)
    # print("Parada nextSlice 1")
    if SUCCS is [] or index == len(SUCCS):
        # print("Parada nextSlice 2")
        return [[], float('inf'), -1]
    if goal_state in SUCCS:
        # print("Parada  nextSlice3")
        return [[], depth + 1, -1]
    SLICE = []
    i = index;
    # print("Parada nextSlice 4")
    while(i < len(SUCCS) and len(SLICE) < B):
        # print("Parada nextSlice 5")
        if(SUCCS[i] not in hash_table):
            # print("Parada nextSlice 6")
            #  Linea 43: depth + 1 (En el PDF hay una errata, no le suma 1)
            ## g(SUCCS[i]) := depth + 1
            SLICE.append(SUCCS[i])
            hash_table.append(SUCCS[i])
            hash_levels.append(depth + 1)
            if len(hash_table) >= memory:
                # print("Parada nextSlice 7")
                for s in SLICE:
                    # print("Parada nextSlice 8")
                    if s in hash_table:
                        # print("Parada nextSlice 9")
                        pos_in_hash_table = hash_table.index(s)
                        # print("hash_table-preborrado: %s" % (hash_table))
                        hash_table.remove(s)
                        # print("hash_table-postborrado: %s" % (hash_table))
                        # print("hash_levels-preborrado: %s" % (hash_levels))
                        hash_levels.pop(pos_in_hash_table)
                        # print("hash_levels-postborrado: %s" % (hash_levels))
                return [[], float('inf'), -1]
        # print("Parada nextSlice 10")
        i = i + 1
    # print("Parada nextSlice 11")
    return [SLICE, -1, i]

# Funciona bien.
# Comprobado con un BEAM de tamaño 1 y 2
# Comprobado con hash_table vacío y con varios estados incluidos
def generateNewSuccessor(stateset, hash_table):

    UnsortedSUCCS = []

    # Generate the SET nodes
    for state in stateset:
        contadoor = 0
        for successor in neighbours(state):
            if successor not in hash_table:
                if successor not in UnsortedSUCCS:
                    UnsortedSUCCS.append(successor)
            contadoor = contadoor + 1

    ## Sort states in SUCCS in order of increasing heuristic values

    if not UnsortedSUCCS:
        return []

    SUCCS = []
    # print("UnsortedSUCCS: %s" % (UnsortedSUCCS))
    currentState = UnsortedSUCCS[0]

    for a in UnsortedSUCCS:
        cS = deepcopy(currentState)
        for eachElelement in UnsortedSUCCS:
            if cS not in SUCCS:
                break
            else:
                cS = deepcopy(eachElelement)
        currentState = deepcopy(cS)

        for state in UnsortedSUCCS:
            if (heuristic(state) < heuristic(currentState)) and (state not in SUCCS):
                currentState = deepcopy(state)
        SUCCS.append(currentState)

    # print("SUCCS: %s" % (SUCCS))
    # print("==========")

    return SUCCS