# BeamSearch w/ Discrepancies from Artificial Intelligence Subject
# Gastar la discrepancias lo antes posible

from copy import deepcopy

import timeit

# Variables globlales que almacenan la heurística y los vecinos de un estado.
global heuristic
global neighbours

# Variable estática que almacena los estados generados.
# Permite almacenar los estados generados de todas las llamadas recursivas.
class Estados_generados():
    num_estados_generados = 0

# Accedemos a variable mediante una instancia.
# Para entenderlo mejor mira la URL que te dejo dónde te explican cómo se usan las variables estáticas en Python.
# URL: http://radek.io/2011/07/21/static-variables-and-methods-in-python/
estados_generados_instance = Estados_generados()

# Variable estática que almacena la memoria usada.
# Permite almacenar todos los estados almacenados que se han ido añadiendo al hashtable en todas las llamadas recursivas.
class Memory_table():
    memory_table = []

# Accedemos a variable mediante una instancia.
# Para entenderlo mejor mira la URL que te dejo dónde te explican cómo se usan las variables estáticas en Python.
# URL: http://radek.io/2011/07/21/static-variables-and-methods-in-python/
memory_table_instance = Memory_table()

# Algoritmo padre.
# Es al que se llama desde N-puzzle y N-crepes.
# Recibe:
    # initial_state: Estado inicial generado de forma aleatoria desde N-puzzle y N-crepes.
    # goal_state: Estado final al que queremos llegar.
    # B: Ancho del Haz que vamos a elegir.
    # memory: Tamaño de la memoria disponible para este problema.
def BULB(initial_state, goal_state, B, memory):

    # Marcador de tiempo inicial.
    start = timeit.default_timer()

    # Initialization:

    # Número de discrepancias del problema.
    discrepancies = 0

    # Variable que aparentamente no se usa.
    # Quizás haya que quitarla xD
    state_level = 0;

    # Tabla dónde almacemos los estados visitados.
    hash_table = [initial_state]

    # Tabla de misma longitud que hash_table que nos dice en qué nivel del árbol está cada estado.
    hash_levels = [0]

    # Nivel máximo de vueltas que puede dar el while de abajo.
    # Sin esta variable, el número de vueltas podría ser casi-infinito.
    limitWhile = 1000000

    # Inicializamos la varible declarada antes como variable estática.
    num_estados_generados = 0

    # Nos indica el tiempo que tarda el algoritmo.
    time = 0

    # print("Parada BULB 1")

    # Bucle dónde se ejecuta el algoritmo.
    while limitWhile != 0:

        # print("^^^^^^^^^^")
        # print("Discrepancia: %s" % (discrepancies))

        # pathlength nos indica la distancia entre el estado inicial al estado final del problema.
        # En otras palabras, es la solución del problema.
        # Llamamos a BULBprobe, que será la propia lógica del algoritmo.
        pathlength = BULBprobe(0, discrepancies, B, hash_table, hash_levels, goal_state, memory, num_estados_generados)

        #print(estados_generados_instance.num_estados_generados)
        #print(len(memory_table_instance.memory_table))

        # No indica si resultado es válido.
        # Si no es infinito significa que tenemos solución.
        if pathlength < float('inf'):
            # Generamos la variable de tiempo de fin del algoritmo.
            stop = timeit.default_timer()
            # Calculamos el tiempo de ejecución del algoritmo.
            time =  stop - start
            # Devolvemos el resultado
            # Originalmente devolvía sólo el pathlength pero es necesario devolver más datos para la ejecución de las pruebas.
            # Devolvemos:
                # 1: Nos indica que hemos encontrado solución. Se puede entrender como boolean haySolucion.
                # pathlength: Resultado propiamente dicho. Es la distancia entre el estado inicial y el final.
                # estados_generados_instance.num_estados_generados: Guardamos el número de estados generados.
                # len(memory_table_instance.memory_table): Guardamos los elementos que han entrado en hash_table.
                    # Ahora me pegunto por qué lo guardo entero y no aumento el contador como hago en la variable anterior.
                # time: Nos indica el tiempo que tarda en ejecutarse el algoritmo.
            return [1, pathlength, estados_generados_instance.num_estados_generados, len(memory_table_instance.memory_table), time]

        # Si el resultado es infinito:
        # Aumentamos el número de discrepancias permitidas.
        discrepancies = discrepancies + 1
        # Disminuimos el número de iteraciones permitidas del while.
        limitWhile = limitWhile - 1
        # Volvemos al while.

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