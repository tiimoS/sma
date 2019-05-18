import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random


G = nx.read_edgelist('facebook_combined.txt')


# Execute 1000 times this command sequence
for step in range(1, 1000):
    # Choose a random start node
    vertexid = 1
    # Dictionary that associate nodes with the amount of times it was visited
    visited_vertices = {}
    # Store and print path
    path = [vertexid]
    
    print("Step: %d" % (step))
    # Restart the cycle
    counter = 0
    # Execute the random walk with size 100 (100 steps)
    for counter in range(1, 100): 
        # Extract vertex neighbours vertex neighborhood
        vertex_neighbors = [n for n in G.neighbors(str(vertexid))]
        # Set probability of going to a neighbour is uniform
        probability = []
        probability = probability + [1./len(vertex_neighbors)] * len(vertex_neighbors)
        # Choose a vertex from the vertex neighborhood to start the next random walk
        vertexid = np.random.choice(vertex_neighbors, p=probability)
        # Accumulate the amount of times each vertex is visited
        if vertexid in visited_vertices:
            visited_vertices[vertexid] += 1
        else:
            visited_vertices[vertexid] = 1

        # Append to path
        path.append(vertexid)
        

    # Organize the vertex list in most visited decrescent order
    mostvisited = sorted(visited_vertices, key = visited_vertices.get,reverse = True)
    print("Path: ", path)
    # Separate the top 10 most visited vertex
    print("Most visited nodes: ", mostvisited[:10])



