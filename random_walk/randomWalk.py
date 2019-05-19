import networkx as nx
import random
from centrality.degree_centrality import highest_degrees_in_community

graph = nx.Graph()


def distribute_messages(graph_network, communities):
    """
    Traverses network from given initial node as random walk. Takes the node and its neighbours and randomly selects
    one. Revisiting already visited nodes is possible
    '''
    :param communities: list of communities
    :param initial_node: initial node to start random walk from
    :return: walked path
    """
    global graph
    graph = graph_network
    walked_paths = []
    # Pick three random communities
    start_communities = []
    for i in range(3):
        community_index = random.randint(0, len(communities) - 1)
        start_communities.append(communities[community_index])

    # Get top user from community
    for community in start_communities:
        top_user = highest_degrees_in_community(graph_network, community)[0]
        walk_path = random_walk(communities, top_user)
        walked_paths.append(walk_path)

    return walked_paths


def random_walk(communities, initial_node):
    """
    Runs random walk from given start node by randomly selecting neighbouring node.
    :param communities: list of communities
    :param initial_node: node with highest degree centrality to randomly selected community.
    :return: walk path i.e. list of nodes visited along the walk
    """
    node_t = initial_node
    visited_communities = set()
    node_dict = node_community_list(communities)
    walk_path = [node_t]
    visited_communities.add(node_dict[node_t])
    while len(communities) > len(visited_communities):
        neighbours = list(graph[node_t])
        random_neighbour_index = random.randint(0, len(neighbours) - 1)
        next_node = neighbours[random_neighbour_index]
        visited_communities.add(node_dict[next_node])
        walk_path.append(next_node)
        node_t = next_node
    return walk_path


def node_community_list(communities):
    """
    Creates dictionary with nodes as keys and communities that they belong to as values
    :param communities: list of communities
    :return: dictionary of nodes and their communities
    """
    node_dict = {}
    for community in communities:
        for node in community.total_nodes:
            node_dict[node.key] = community
    return node_dict



'''
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
            probability = probability + [1. / len(vertex_neighbors)] * len(vertex_neighbors)
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
        mostvisited = sorted(visited_vertices, key=visited_vertices.get, reverse=True)
        print("Path: ", path)
        # Separate the top 10 most visited vertex
        print("Most visited nodes: ", mostvisited[:10])
        print(nx.info(G))
'''
