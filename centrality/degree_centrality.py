import networkx as nx
from collections import defaultdict

graph = nx.read_edgelist('data/testgraph2.txt')
community_top_users = defaultdict(list)
nr_top_users = 2


def top_users(communities):
    """
    Returns the n top users (in our case n=2) with the highest centralityiii degree from each community.
    :param communities: list of communities
    :return: a dictionary of community top users with the community as key and the list of top users as values
    """
    for community in communities:
        top_users = highest_degrees_in_community(community)
        community_top_users[community.key] = top_users
    return community_top_users


def highest_degrees_in_community(community):
    """
    Returns the highest n top users from single community based on degree centralityiii
    :param community: Community object holding the node objects
    :return: a list of the n top user's node keys
    """
    sorted_community_nodes = list(sorted(community.total_nodes, key=lambda node: node.degree, reverse=True))

    top_users = []
    for i in range(nr_top_users):
        top_users.append(sorted_community_nodes[i].key)
    return top_users
