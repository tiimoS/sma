from centrality.degree_centrality import top_users
from louvain.Louvain_detection import louvain_method
from visualization.Visualizer import visualize_network
from random_walk.randomWalk import distribute_messages

import networkx as nx


graph = nx.read_edgelist('data/testgraph2.txt')
#graph = nx.read_edgelist('data/facebook_combined.txt')


def main():
    communities = louvain_method(graph)
    visualize_network(graph, "sample.pdf", communities)
    top_users_in_communities = top_users(graph, communities)
    for community in top_users_in_communities:
        print('Community ', community, ' Top Users: ', top_users_in_communities[community])

    # random walks is a 2D array containing the three paths that were walked during the three walks
    random_walks = distribute_messages(graph, communities)
    for walk in random_walks:
        print('Random Walk: ', walk)


    # visualize the output of applying Random Walk algorithm, by highlighting the sequence of nodes selected in a path
    


if __name__ == '__main__':
    main()
