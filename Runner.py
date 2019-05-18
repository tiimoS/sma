from centrality.degree_centrality import top_users
from louvain.Louvain_detection import louvain_method
from louvain.Louvain_detection import visualize_network


def main():
    communities = louvain_method()
    visualize_network("sample.pdf", communities)
    top_users_in_communities = top_users(communities)
    print('Top user dictionary: ', top_users_in_communities)


if __name__ == '__main__':
    main()
