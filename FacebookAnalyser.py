from __future__ import division  # to make sure that divisions result in floating points

import networkx as nx


def main():
    G = load_graph();
    louvain_detection(G);


def load_graph():
    # G = nx.read_edgelist('facebook_combined.txt')
    G = nx.read_edgelist('testgraph2.txt')
    # print(nx.info(G));
    return G


def louvain_detection(G):
    communities = []
    new_communities = []

    nodes = []
    for node in G.nodes:
        nodes.append([node])
        communities.append([node])
        new_communities.append([node])

    iterations = 0
    while True:
        # Initialize two lists to keeping track of current and new communities.
        # Initially, each node forms its own community
        new_communities = louvain_iteration(G, new_communities, nodes)
        iterations+=1
        if new_communities == communities:
            nodes = new_communities
            print('iterations: ', iterations)
            print('\n********************************************************************\n\n')
            new_communities = louvain_iteration(G, new_communities, nodes)
            break
        else:
            communities = new_communities


def louvain_iteration(G, new_communities, nodes):
    for node_i in nodes:
        print('Nodes: ', nodes)
        print('communities: ', new_communities)
        print('\tnode_i: ', node_i)

        new_communities = remove_node(new_communities, node_i)
        neighbouring_communities = get_neighbouring_communities(G, node_i, new_communities)
        degree_i = get_degree_i(G, node_i, neighbouring_communities)
        print('\tremoved communities: ', new_communities)
        print('\tnode_i: ', node_i)
        print('\tDegree_i: ', degree_i)
        print('\tNeighbours: ', neighbouring_communities, '\n')

        # get modularity gain for each neighbouring community
        max_modularity_gain = 0
        best_community = node_i

        for neighbour in neighbouring_communities:
            print('\t\tNeighbouring community: ', neighbour)
            degree_j = get_degree_j(G, node_i, neighbour, new_communities)
            d_ij = get_shared_edge_weight(G, node_i, neighbour)

            print('\t\t\tdegree_j: ', degree_j)
            print('\t\t\td_ij: ', d_ij)
            mod_gain = modularity_gain(G, degree_i, degree_j, d_ij)
            print('\t\t\tmod gain: ', mod_gain)
            if max_modularity_gain < mod_gain:
                max_modularity_gain = mod_gain
                best_community = neighbour
            print('\t\t\tbest community: ', best_community)

        # insert node_i into maximizing community.
        insert_nodes(best_community, new_communities, node_i)
        print('new communities: ', new_communities, '\n\n')
    return new_communities


def insert_nodes(best_community, new_communities, node_i):
    index = new_communities.index(best_community)
    new_communities.pop(index)
    for node in node_i:
        best_community.append(node)
    new_communities.append(best_community)


def modularity_gain(G, degree_i, degree_j, d_ij):
    m = G.number_of_edges()
    modularity_gain = 1.0 / (2 * m) * (d_ij - degree_i * degree_j / m)
    return modularity_gain


def get_neighbouring_communities(G, node_i, communities):
    neighbouring_communities = []
    for node in node_i:
        neighbours = G[node]
        for neighbour in neighbours:
            for community in communities:
                if neighbour in community:
                    if community not in neighbouring_communities:
                        neighbouring_communities.append(community)
    return neighbouring_communities


def get_degree_i(G, node_i, neighbours):
    if len(node_i) == 1:
        return G.degree(node_i[0])  # get degree of node i
    else:
        print('neighbours for degree: ', neighbours)
        degree_i = len(neighbours)
        return degree_i


def get_degree_j(G, node_i, node, communities):
    if len(node_i) == 1:
        degree_j = 0
        for n in node:
            degree_j += G.degree(n)
    else:
        neighbours = get_neighbouring_communities(G, node, communities)
        degree_j = len(neighbours)
    return degree_j


def get_shared_edge_weight(G, node_i, neighbour):
    d_ij = 0
    if len(node_i) == 1:
        for node in neighbour:
            if G.has_edge(node_i[0], node):
                d_ij += 2
    else:
        d_ij = 2
    return d_ij


def remove_node(communities, node_i):
    print('node_i: ', node_i)

    if len(node_i) == 1:
        for community in communities:
            if node_i[0] in community:
                community.pop(community.index(node_i[0]))
    else:
        if node_i in communities:
            communities.pop(communities.index(node_i))

    communities = [x for x in communities if x != []]

    return communities


if __name__ == '__main__':
    main()