# BeamSearch w/ Discrepancies from Artificial Intelligence Subject
# Gastar la discrepancias lo antes posible

global heuristic
global neighbours

def BULB(initial_state, goal_state, heuristic, B, memory):

    # Initialization
    discrepancies = 0
    state_level = 0;
    hash_table = [initial_state]

    while True:
        pathlength = BULBprobe(0, discrepancies, heuristic, B, hash_table, goal_state, memory)
        if pathlength < float('inf'):
            return pathlength
        discrepancies = discrepancies + 1

def BULBprobe(depth, discrepancies, heuristic, B, hash_table, goal_state, memory):

    [SLICE, value, index] = nextSlice(depth, 0, heuristic, B, hash_table, goal_state, memory)

    if value >= 0:
        return value

    if discrepancies == 0:
        if SLICE is []:
            return float('inf')
        pathlenght = BULBprobe(depth+1, 0, heuristic, B, hash_table, goal_state, memory)
        for s in SLICE:
            hash_table.remove(s)
        return pathlenght
    else:
        if SLICE is not []:
            for s in SLICE:
                hash_table.remove(s)
        while True:
            [SLICE, value, index] = nextSlice(depth, index, heuristic, B, hash_table, goal_state, memory)
            if value >= 0:
                if value < float('inf'):
                    return value
                else:
                    break
            if SLICE is []:
                continue
            pathlenght = BULBprobe(depth+1, discrepancies-1, heuristic, B, hash_table, goal_state, memory)
            for s in SLICE:
                hash_table.remove(s)
            if pathlenght < float('inf'):
                return pathlenght
        [SLICE, value, index] = nextSlice(depth, 0, heuristic, B, hash_table, goal_state, memory)
        if value >= 0:
            return value
        if SLICE is []:
            return float('inf')
        pathlenght = BULBprobe(depth+1, discrepancies, heuristic, B, hash_table, goal_state, memory)
        for s in SLICE:
            hash_table.remove(s)
        return pathlenght

def nextSlice(depth, index, heuristic, B, hash_table, goal_state, memory):

    # g() obtener el nivel del estado: Sacar de la memoria el bloque que está en el nivel s # Linea 43: depth + 1

    ## currentlayer := {s in hash_table | g(s) = depth}
    SUCCS = generateNewSuccessor(currentlayer, heuristic, hash_table)
    if SUCCS is [] or index == len(SUCCS):
        return [[], float('inf'), -1]
    if goal_state in SUCCS:
        return [[], depth + 1, -1]
    SLICE = []
    i = index;
    while(i < len(SUCCS) and len(SLICE) < B):
        if(SUCCS[i] not in hash_table):
            ## g(SUCCS[i]) := depth + 1
            SLICE.append(SUCCS[i])
            hash_table.append(SUCCS[i])
            if len(hash_table) >= memory:
                for s in SLICE:
                    hash_table.remove(s)
                return [[], float('inf'), -1]
        i = i + 1
    return [SLICE, -1, i]

def generateNewSuccessor(stateset, heuristic, hash_table):

    index = 0
    SUCCS = []
    for state in stateset:
        for successor in state:
            if successor not in hash_table:
                SUCCS[index] = successor;
                index = index + 1

    # Sort states in SUCCS in order of increasing heuristic values

    return SUCCS