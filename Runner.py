from centrality.degree_centrality import top_users
from louvain.Louvain_detection import louvain_method
from visualization.Visualizer import visualize_network
from random_walk.randomWalk import distribute_messages


import networkx as nx


graph = nx.read_edgelist('data/testgraph2.txt')
#graph = nx.read_edgelist('data/facebook_combined.txt')


def main():
    communities = louvain_method(graph)
    visualize_network(graph, "louvain_communities.pdf", communities, [], [])
    top_users_in_communities = top_users(graph, communities)
    for community in top_users_in_communities:
        print('Community ', community, ' Top Users: ', top_users_in_communities[community])

    # random walks is a 2D array containing the three paths that were walked during the three walks
    random_walks = distribute_messages(graph, communities)
    edge_colors = ['r', 'g', 'b']
    j = 0
    for walk in random_walks:
        print('\nRandom Walk: Visited ', len(walk), ' nodes - ', walk)
        color = edge_colors[j]
        j += 1
        file_name = 'random_walk' + str(j) + '.pdf'
        visualize_network(graph, file_name, communities, walk, color)


if __name__ == '__main__':
    main()
