# BeamSearch w/ Discrepancies from Artificial Intelligence Subject
# Gastar la discrepancias lo antes posible

from copy import deepcopy

import timeit

global heuristic
global neighbours

class Estados_generados():
    num_estados_generados = 0

estados_generados_instance = Estados_generados()

class Memory_table():
    memory_table = []

memory_table_instance = Memory_table()

def BULB(initial_state, goal_state, B, memory):

    start = timeit.default_timer()

    # Initialization
    discrepancies = 0
    state_level = 0;
    hash_table = [initial_state]
    hash_levels = [0]
    limitWhile = 1000000
    num_estados_generados = 0
    time = 0


    # print("Parada BULB 1")
    while limitWhile != 0:
        # print("^^^^^^^^^^")
        # print("Discrepancia: %s" % (discrepancies))
        pathlength = BULBprobe(0, discrepancies, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)
        #print(estados_generados_instance.num_estados_generados)
        #print(len(memory_table_instance.memory_table))
        if pathlength < float('inf'):
            stop = timeit.default_timer()
            time =  stop - start
            return [1, pathlength, estados_generados_instance.num_estados_generados, len(memory_table_instance.memory_table), time]
        discrepancies = discrepancies + 1
        limitWhile = limitWhile - 1

def BULBprobe(depth, discrepancies, B, hash_table, hash_levels, goal_state, memory,num_estados_generados):

    # print("Hash Table: %s" % (hash_table))
    # print("Hash Levels: %s" % (hash_levels))

    [SLICE, value, index] = nextSlice(depth, 0, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)

    # print("SLICE: %s" % (SLICE))
    # print("value: %s" % (value))
    # print("index: %s" % (index))

    if value >= 0:
        return value

    if discrepancies == 0:
        if SLICE is []:
            return float('inf')
        pathlenght = BULBprobe(depth+1, 0, B, hash_table, hash_levels, goal_state, memory,num_estados_generados)
        for s in SLICE:
            if s in hash_table:
                pos_in_hash_table = hash_table.index(s)
                hash_table.remove(s)
                # memory_table_instance.memory_table.remove(s)
                hash_levels.pop(pos_in_hash_table)
        return pathlenght
    else:
        if SLICE is not []:
            for s in SLICE:
                if s in hash_table:
                    pos_in_hash_table = hash_table.index(s)
                    hash_table.remove(s)
                    # memory_table_instance.hash_table2.remove(s)
                    hash_levels.pop(pos_in_hash_table)
        while True:
            [SLICE, value, index] = nextSlice(depth, index, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)
            if value >= 0:
                if value < float('inf'):
                    return value
                else:
                    break
            if SLICE is []:
                continue
            pathlenght = BULBprobe(depth+1, discrepancies-1, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)
            for s in SLICE:
                if s in hash_table:
                    pos_in_hash_table = hash_table.index(s)
                    hash_table.remove(s)
                    # memory_table_instance.memory_table.remove(s)
                    hash_levels.pop(pos_in_hash_table)
            if pathlenght < float('inf'):
                return pathlenght
        [SLICE, value, index] = nextSlice(depth, 0, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)
        if value >= 0:
            return value
        if SLICE is []:
            return float('inf')
        pathlenght = BULBprobe(depth+1, discrepancies, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)
        for s in SLICE:
            if s in hash_table:
                pos_in_hash_table = hash_table.index(s)
                hash_table.remove(s)
                # memory_table_instance.memory_table.remove(s)
                hash_levels.pop(pos_in_hash_table)
        return pathlenght

def nextSlice(depth, index, B, hash_table, hash_levels, goal_state, memory, num_estados_generados):

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


    SUCCS = generateNewSuccessor(currentlayer, hash_table, num_estados_generados)
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
            memory_table_instance.memory_table.append(SUCCS[i])
            hash_levels.append(depth + 1)
            if len(hash_table) >= memory:
                for s in SLICE:
                    if s in hash_table:
                        pos_in_hash_table = hash_table.index(s)
                        hash_table.remove(s)
                        memory_table_instance.memory_table.remove(s)
                        hash_levels.pop(pos_in_hash_table)
                return [[], float('inf'), -1]
        i = i + 1
    return [SLICE, -1, i]

# Funciona bien.
# Comprobado con un BEAM de tamaño 1 y 2
# Comprobado con hash_table vacío y con varios estados incluidos
def generateNewSuccessor(stateset, hash_table, num_estados_generados):

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

    estados_generados_instance.num_estados_generados = estados_generados_instance.num_estados_generados + len(SUCCS)

    return SUCCS