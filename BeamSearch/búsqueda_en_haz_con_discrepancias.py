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

    while limitWhile != 0:
        pathlength = BULBprobe(0, discrepancies, B, hash_table, hash_levels, goal_state, memory)
        if pathlength < float('inf'):
            return pathlength
        discrepancies = discrepancies + 1
        limitWhile = limitWhile - 1

def BULBprobe(depth, discrepancies, B, hash_table, hash_levels, goal_state, memory):

    [SLICE, value, index] = nextSlice(depth, 0, B, hash_table, hash_levels, goal_state, memory)

    if value >= 0:
        return value

    if discrepancies == 0:
        if SLICE is []:
            return float('inf')
        pathlenght = BULBprobe(depth+1, 0, B, hash_table, hash_levels, goal_state, memory)
        for s in SLICE:
            hash_table.remove(s)
        return pathlenght
    else:
        if SLICE is not []:
            for s in SLICE:
                hash_table.remove(s)
        while True:
            [SLICE, value, index] = nextSlice(depth, index, B, hash_table, hash_levels, goal_state, memory)
            if value >= 0:
                if value < float('inf'):
                    return value
                else:
                    break
            if SLICE is []:
                continue
            pathlenght = BULBprobe(depth+1, discrepancies-1, B, hash_table, hash_levels, goal_state, memory)
            for s in SLICE:
                hash_table.remove(s)
            if pathlenght < float('inf'):
                return pathlenght
        [SLICE, value, index] = nextSlice(depth, 0, B, hash_table, hash_levels, goal_state, memory)
        if value >= 0:
            return value
        if SLICE is []:
            return float('inf')
        pathlenght = BULBprobe(depth+1, discrepancies, B, hash_table, hash_levels, goal_state, memory)
        for s in SLICE:
            hash_table.remove(s)
        return pathlenght

def nextSlice(depth, index, B, hash_table, hash_levels, goal_state, memory):

    ## currentlayer := {s in hash_table | g(s) = depth}

    currentlayer = []
    pos_in_list = 0

    # g() obtener el nivel del estado: Sacar de la memoria el bloque que está en el nivel s
    for i in hash_levels:
        if i == depth:
            currentlayer.append(hash_table[pos_in_list])
        pos_in_list = pos_in_list + 1


    SUCCS = generateNewSuccessor(currentlayer, hash_table)
    if SUCCS is [] or index == len(SUCCS):
        return [[], float('inf'), -1]
    if goal_state in SUCCS:
        return [[], depth + 1, -1]
    SLICE = []
    i = index;
    while(i < len(SUCCS) and len(SLICE) < B):
        if(SUCCS[i] not in hash_table):
            #  Linea 43: depth + 1 (En el PDF hay una errata, no le suma 1)
            ## g(SUCCS[i]) := depth + 1
            SLICE.append(SUCCS[i])
            hash_table.append(SUCCS[i])
            hash_levels.append(depth + 1)
            if len(hash_table) >= memory:
                for s in SLICE:
                    if s in hash_table:
                        pos_in_hash_table = hash_table.index(s)
                        hash_table.remove(s)
                        hash_levels.pop(pos_in_hash_table)
                return [[], float('inf'), -1]
        i = i + 1
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

    SUCCS = []
    print("UnsortedSUCCS: %s" % (UnsortedSUCCS))
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

    print("SUCCS: %s" % (SUCCS))

    return SUCCS