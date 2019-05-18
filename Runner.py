from centrality.degree_centrality import top_users
from louvain.Louvain_detection import louvain_method
from louvain.Louvain_detection import visualize_network
from random_walk.randomWalk import distribute_messages


def main():
    communities = louvain_method()
    visualize_network("sample.pdf", communities)
    top_users_in_communities = top_users(communities)
    for community in top_users_in_communities:
        print('Community ', community, ' Top Users: ', top_users_in_communities[community])

    # random walks is a 2D array containing the three paths that were walked during the three walks
    random_walks = distribute_messages(communities)
    for walk in random_walks:
        print('Random Walk: ', walk)

if __name__ == '__main__':
    main()
