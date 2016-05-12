# BeamSearch from Artificial Intelligence Subject

# Important data:
#   h -> Heuristic function
#   B -> The number of nodes that are stored at each level of the Breadth-First Search.
#   BEAM -> Store the nodes that are to be expanded in the next loop of the algorithm.
#   hash_table  -> Store nodes that have been visited.
#   g -> Used to keep track of the depth of the search, which is the cost of reaching a node at that level.

# How it works:
# - Each time through the main loop of the algorithm, Beam Search adds all of the nodes connected to the nodes in the BEAM to its SET of successor nodes and then adds the B nodes with the best heuristic values from the SET to the BEAM and the hash table.
# - Note that a node that is already in the hash table is not added to the BEAM because a shorter path to that node has already been found.
# - This process continues until the goal node is found, the hash table becomes full (indicating that the memory available has been exhausted), or the BEAM is empty after the main loop has completed (indicating a dead end in the search).

