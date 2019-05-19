from centrality.degree_centrality import top_users
from centrality.degree_centrality import highest_degrees_in_community
from louvain.Louvain_detection import louvain_method
from visualization.Visualizer import visualize_louvain
from visualization.Visualizer import visualize_randomWalk
from random_walk.randomWalk import distribute_messages

import networkx as nx


graph = nx.read_edgelist('data/testgraph2.txt')
#graph = nx.read_edgelist('data/facebook_combined.txt')


def main():
    # Call Louvain method
    communities = louvain_method(graph)

    # Visualize the network
    visualize_louvain(graph, "sample1", communities)
    visualize_randomWalk(graph, "sample2.pdf", communities)

    # Identify top 2 users with the highest degree centrality in each community.
    top_users_in_communities = top_users(graph, communities)
    for community in top_users_in_communities:
        print('Community ', community, ' Top Users: ', top_users_in_communities[community])

    # random walks is a 2D array containing the three paths that were walked during the three walks
    random_walks = distribute_messages(graph, communities)
    for walk in random_walks:
        print('Random Walk: ', walk)


if __name__ == '__main__':
    main()
