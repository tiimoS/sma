from centrality.degree_centrality import top_users
from louvain.Louvain_detection import louvain_method
from visualization.Visualizer import visualize_network
from random_walk.randomWalk import distribute_messages


import networkx as nx


#graph = nx.read_edgelist('data/testgraph2.txt')
graph = nx.read_edgelist('data/facebook_combined.txt')


def main():
    communities = louvain_method(graph)
    visualize_network(graph, "louvain_communities.pdf", communities, [], [])
    find_top_users(communities)
    run_random_walks(communities)


def run_random_walks(communities):
    random_walks = distribute_messages(graph, communities)
    edge_colors = ['r', 'g', 'b']
    j = 0
    for walk in random_walks:
        print('Random Walk: Visited ', len(walk), ' nodes - ', walk)
        color = edge_colors[j]
        j += 1
        file_name = 'random_walk' + str(j) + '.pdf'
        visualize_network(graph, file_name, communities, walk, color)


def find_top_users(communities):
    top_users_in_communities = top_users(graph, communities)
    for community in top_users_in_communities:
        print('Community ', community)
        user_dict = top_users_in_communities[community]
        for user, degree in user_dict.items():
            print('\tTop User: ', user, ', Degree Centrality: ', degree)
    print('\n')


if __name__ == '__main__':
    main()
