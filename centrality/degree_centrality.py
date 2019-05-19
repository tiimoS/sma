import networkx as nx
from collections import defaultdict

graph = nx.Graph()
community_top_users = defaultdict(list)
nr_top_users = 2


def top_users(graph_network, communities):
    """
    Returns the n top users (in our case n=2) with the highest old_centrality degree from each community.
    :param communities: list of communities
    :return: a dictionary of community top users with the community as key and the list of top users as values
    """
    global graph
    graph = graph_network
    for community in communities:
        top_users = highest_degrees_in_community(graph_network, community)
        community_top_users[community.key] = top_users
    return community_top_users


def highest_degrees_in_community(graph_network, community):
    """
    Returns the highest n top users from single community based on degree old_centrality
    :param community: Community object holding the node objects
    :return: a list of the n top user's node keys
    """
    global graph
    graph = graph_network
    sorted_community_nodes = list(sorted(community.total_nodes, key=lambda node: node.degree, reverse=True))

    top_users = []
    for i in range(nr_top_users):
        top_users.append(sorted_community_nodes[i].key)
    return top_users
