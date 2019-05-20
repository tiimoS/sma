from __future__ import division
from collections import defaultdict

import networkx as nx
import time
import math


graph = nx.Graph()
m = 0
graph_nodes = {}
community_dict = {}


def louvain_method(graph_network):
    """
    Runs the louvain algorithm over the nodes of the networks and e.g. forms new communities that maximize the
    modularity gain. First, it creates a single node community for each node in the network. We then iterate over all
    nodes. For each node, we remove it from its community, get its neighbouring communities, calculates the modularity
    gain of putting the node into these communities and the picks the one with the highest gain. We repeat this process
    as long as there are nodes that change partitions. When the partitions i.e. communities don't change anymore (end
    of first passage), we create hypernodes from our communities and repeat the whole process again (second passage).
    We repeat the iterations and hypernode creations as long as there is a positive modularity gain i.e. the communities
    change.

    :return: a list of communities for the network
    """
    global graph, m
    graph = graph_network
    m = graph.number_of_edges()
    repeat_louvain = True
    is_hyperrun = False
    passage = 0
    dendrogram = defaultdict(list)
    total_start_time = time.time()

    # louvain algorithm: merges communities and creates hyper-nodes as long as there is a positive modularity gain
    # and as long as communities still change and there are more than one community left.
    while repeat_louvain:
        passage += 1
        print('\nPassage ', passage, ':')

        if is_hyperrun:  # if we are in the hypernode stage, create hypernodes from communities
            nodes = create_hypernodes(communities)
        else:  # single node communities
            nodes = create_node_objects(graph.nodes)
            for node in nodes:
                node.total_nodes.add(node)

        communities = turn_nodes_into_communities(nodes)

        if not is_hyperrun:
            old_mod = modularity(communities)

        # start the louvain algorithm for given list of communities and nodes
        passage_start_time = time.time()
        communities, iteration, new_mod = louvain_passage(communities, nodes)
        passage_end_time = round((time.time() - passage_start_time) * 1000, 3)

        dendrogram[passage] = communities.copy()

        # Termination criterion: as long as new modularity is higher than the old modularity
        if new_mod < old_mod:
            repeat_louvain = False
            communities = dendrogram[passage - 1]  # communities from previous passage are optimal
        else:
            old_mod = new_mod

        print_communities(communities, iteration, passage_end_time)
        is_hyperrun = True  # from now on working with hypernodes

    total_end_time = round((time.time() - total_start_time) * 1000, 3)
    print('\nTotal performance time louvain method: ', total_end_time, 'ms')
    print('Total number of communities detected: ', len(communities), ' Communities')
    print('Modularity: ', old_mod, '\n')
    return communities


def louvain_passage(communities, nodes):
    """
    Iterates over all nodes of a given list and runs the louvain iterations ie. removes the node from its community,
    gets the neighbouring communities and find the community maximizing the modularity gain. Then it adds the node to
    the found community. It repeats the process as long as the partitions change
    :param communities: list of communities of the network
    :param nodes: list of nodes to iterate over
    :return: (updated) list of communities
    """
    updated = True
    iteration = 0
    while updated:  # iterate as long as the partitions change during the iteration
        updated = False  # keeps track of whether a community changed during the iteration or not
        iteration += 1
        print('\tIteration ', iteration, '...')
        for node in nodes:
            community = community_dict[node.key]  # get the community that the node belongs to
            prev_community = id(community)  # get the id of the community to compare later on

            community.remove_node(node)  # removes the nodes from the community
            max_community = find_maximizing_community(node)  # returns the community with the highest modularity gain
            max_community.add_node(node)  # adds the node to the community with the highest modularity gain

            new_community = id(max_community)  # gets the ID of the new community
            if prev_community != new_community:  # if the node belongs to a different community, mark updated as true
                updated = True

            # remove redundant empty communities from the list of communities
            if len(community.nodes) == 0:
                communities.remove(community)
    modularity = get_total_modularity(communities)
    return communities, iteration, modularity


def get_total_modularity(communities):
    """
    Updates the list of neighbours to be the list of neighbouring communities, updates the number of internal links
    and calculates the modularity of the new communities.
    :param communities: list of generated communities
    :return: modularity of new communities
    """
    for community in communities:
        neighbours = {}
        for neighbour in community.neighbouring_communities:
            neigh_community = community_dict[neighbour]
            if neigh_community.key in neighbours:
                neighbours[neigh_community.key] += community.neighbouring_communities[neighbour]
            else:
                neighbours[neigh_community.key] = community.neighbouring_communities[neighbour]
        community.neighbouring_communities = neighbours

        internal_links = 0
        community.total_degree = 0
        for node in community.total_nodes:
            community.total_degree += node.degree
            for node_j in community.total_nodes:
                if node != node_j:
                    if graph.has_edge(node.key, node_j.key):
                        internal_links += 1
            community.internal_links = internal_links/2
    mod = modularity(communities)
    return mod


def print_communities(communities, iteration, perf_time):
    """
    Prints the results of a passage to the console, including the list and number of communities, the number of iterations
    that were required and the time elapsed for completing the passage.
    :param communities: list of communities of the network including the nodes belonging to them
    :param iteration: int - number of iterations required to complete the passage (until partitions did not change anymore)
    :param perf_time: time required to complete the passage.
    """
    for community in communities:
        print('\t\tCommunity: ', community)
    print('\tIn total ', iteration, ' iterations, resulting in ', len(communities), ' communities')
    print('\tTotal time elapsed: ', perf_time, 'ms')


def create_node_objects(node_keys):
    """
    Creates Node objects to given node keys. The Node objects are used to hold the important characteristics of each
    node, such as the degree or the neighbours.
    :param node_keys: strings, keys from the networkx graph representing the node, usually as a digit e.g. 1, 7, 10
    :return: the list of all node objects belonging to the network
    """
    nodes = []
    for key in node_keys:
        node = Node(key)
        node.degree = graph.degree(key)
        node.neighbours = init_neighbours(key)
        nodes.append(node)
        graph_nodes[key] = node
    return nodes


def create_hypernodes(communities):
    """
    Creates hypernode object from community objects. Takes over the nodes belonging to the community and adds them to the
    list of total nodes, takes over the communities neighbours and updates them to be the neighbouring communities incl.
    updating the edge count. The new degree corresponds to the number of neighbouring communities (one edge per neighbouring
    community).
    :param communities: list of communities containing node objects from previous passage
    :return: list of newly created hypernodes based on previous communities
    """
    nodes = []
    for community in communities:
        node = Node(community.key)
        node.neighbours = community.neighbouring_communities
        node.degree = community.total_degree
        nodes.append(node)
        node.total_nodes = community.total_nodes
    return nodes


def turn_nodes_into_communities(nodes):
    """
    Creates Community objects each holding exactly one Node object i.e. single node communities. We update the list
    of nodes belonging to the community, the total community degree and the list of neighbouring nodes. Last, we
    add the community object to the list of all communities in the network
    :param nodes: list of Node objects belonging to the network
    :return: list of Community objects belonging to the network
    """
    global m
    communities = []
    for node in nodes:
        community = Community(node.key)
        community.nodes[node.key] = 1
        community_dict[node.key] = community  # assign node to community
        for neighbour_key in node.neighbours:  # add neighbours of node to list of neighbours of the community
            # take over the nodes neighbouring communities as the communities neighbouring communities
            if neighbour_key in community.neighbouring_communities:
                community.neighbouring_communities[neighbour_key] += node.neighbours[neighbour_key]
            else:
                community.neighbouring_communities[neighbour_key] = node.neighbours[neighbour_key]

        community.total_degree = node.degree
        node.degree = len(node.neighbours)
        community.degree = node.degree
        community.size = 1
        communities.append(community)

        # take over all children nodes from hyper-nodes
        for child_node in node.total_nodes:
            community.total_nodes.add(child_node)
    return communities


def edge_count(communities):
    global m
    graph_edges = set()
    for community in communities:
        for neighbour_key in community.neighbouring_communities:
            # count the edges in the new hyper-graph
            if community.key < neighbour_key:
                graph_edges.add(community.key + neighbour_key)
            else:
                graph_edges.add(neighbour_key + community.key)
    m = len(graph_edges)


def find_maximizing_community(node):
    """
    Gets all the neighbouring communities of a node and calculates the modularity gain for each neighbouring community.
    :param node: Node object that we want to move to the community with the highest modularity gain.
    :return: the community object with the highest modularity gain for the node
    """
    global m
    degree_i = node.degree
    max_modularity_gain = 0  # only update the community, if there is a positive modularity gain
    best_fitting_community = community_dict[node.key]

    # get neighbouring communities of node
    for neighbour_key in node.neighbours:
        neighbouring_community = community_dict[neighbour_key]  # gets the neighbour's community
        degree_j = neighbouring_community.degree

        # to get the shared edge weight, we simply get the communities reference counter to the corresponding node,
        # then we know how many nodes in the community have an edge to the given node
        d_ij = 2 * neighbouring_community.neighbouring_communities[node.key]
        modularity_gain = 1.0 / (2 * m) * (d_ij - degree_i * degree_j / m)
        if max_modularity_gain < modularity_gain:
            max_modularity_gain = modularity_gain
            best_fitting_community = neighbouring_community
    return best_fitting_community


def modularity(communities):
    """
    Calculates the communities modularity using the number of internal links
    :param communities:
    :return:
    """
    global m
    mod = 0
    for community in communities:
        mod += ((community.internal_links / m) - math.pow(community.total_degree/(2*m), 2))
    return mod


class Node:
    key: str
    degree: int

    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.neighbours = {}
        self.total_nodes = set()
        self.internal_links = 0

    def __str__(self) -> str:
        return self.key


def init_neighbours(key):
    """
    Sets then neighbouring nodes and initializes the edge count to the neighbours to 1
    :param key: str - key of node to which we are searching the neighbours
    :return: dictionary of neighbours with corresponding edge count
    """
    neighbours = {}
    neighbouring_nodes = graph[key]
    for node in neighbouring_nodes:
        if neighbouring_nodes[node] == {}:
            neighbours[node] = 1
        else:
            neighbours[node] = neighbouring_nodes[node]
    return neighbours


class Community:
    key: str
    degree: int

    def __init__(self, key):
        self.key = key
        self.nodes = {}
        self.total_nodes = set()
        self.neighbouring_communities = {}
        self.internal_links = 0
        self.degree = 0
        self.total_degree = 0
        self.size = 0

    def __str__(self) -> str:
        return self.key

    def add_node(self, node):
        """
        Adds a Node object to the community and updates all required fields such as total community degree, list of
        neighbours or list of nodes belonging to the community.
        :param node: Node object to be added to the community
        """
        # the neighbouring community counter keeps track of how many nodes in the community have an edge to the node
        # we want to add to the community. So we simply move this counter to the list of node counters of the community,
        # increment it and delete the neighbour reference counter
        self.nodes[node.key] = self.neighbouring_communities[node.key] + 1
        self.internal_links += self.neighbouring_communities[node.key] - 1
        del self.neighbouring_communities[node.key]

        # update the community the node belongs to
        community_dict[node.key] = self

        # Add all neighbours of node we're adding to the community to list of community neighbours and update edge count
        self.add_node_neighbours(node)

        # add all nodes belonging to possible hypernodes to the communities list of nodes
        for child_node in node.total_nodes:
            self.total_nodes.add(child_node)

        # Update the community degree and size
        self.degree += node.degree
        self.size += 1

        # update the string representation of the community
        self.updated_string_representation()

    def add_node_neighbours(self, node):
        """
        Adds all neighbours of node to the community list of neighbours and updates the edge counters.
        :param node: Node object to be added to the community
        """
        for neighbour_key in node.neighbours:
            if neighbour_key not in self.nodes:  # if the node's neighbour is not part of the community
                if neighbour_key in self.neighbouring_communities:
                    self.neighbouring_communities[neighbour_key] += node.neighbours[neighbour_key]
                else:  # if a neighbour of the node we're adding, belongs to the community, update the node counter
                    self.neighbouring_communities[neighbour_key] = node.neighbours[neighbour_key]
            else:  # the neighbour of the node is already present in the the list of neighbouring communities -> update
                self.nodes[neighbour_key] += node.neighbours[neighbour_key]

    def remove_node(self, node2remove):
        """
        Removes a node object form the assigned community, updates all fields such as total degree, list of nodes and
        list of neighbours.
        :param node2remove: the node object we want to remove from the community
        """
        # remove the node from the list of nodes belonging to the community by decrementing the node counter
        self.nodes[node2remove.key] -= 1

        # remove node2remove and all possible sub-nodes belonging to it (hypernode) from the total list of nodes
        for child_node in node2remove.total_nodes:
            self.total_nodes.discard(child_node)

        # add the node we remove from the community to the list of community neighbours
        self.neighbouring_communities[node2remove.key] = self.nodes[node2remove.key]
        self.internal_links -= self.nodes[node2remove.key] - 1
        del self.nodes[node2remove.key]

        # update the dict of neighbouring communities, i.e. decrement the counter of neighbours or nodes of the
        # community that are neighbours of the node we are removing. If the counter gets 0, we remove the entry
        self.remove_node_neighbours(node2remove)

        # update the degree of the community, by subtracting the node's degree
        self.degree -= node2remove.degree
        self.size -= 1

        # update the string representation of the community
        self.updated_string_representation()

    def remove_node_neighbours(self, node2remove):
        """
        Removes all neighbours of the node2remove from the list of community neighbours i.e. it updates the edge
        count of these neighbours and removes them if the count gets 0.
        :param node2remove: node object to be removed from the community
        :return: updated dictionary of neighbours
        """
        for neighbour_key in node2remove.neighbours:
            # update the node reference counter
            if neighbour_key in self.nodes:
                self.nodes[neighbour_key] -= node2remove.neighbours[neighbour_key]
            else:
                self.neighbouring_communities[neighbour_key] -= node2remove.neighbours[neighbour_key]
                if self.neighbouring_communities[neighbour_key] == 0:
                    del self.neighbouring_communities[neighbour_key]

    def updated_string_representation(self):
        """
        Iterates over all nodes belonging to the community and adds their string representation to the string
        representation of the community. Mainly used for nice console output whilst running the algorithm
        :return: string representation of the community i.e. string with all node keys belonging to community
        """
        self.key = ""
        for node in self.total_nodes:
            self.key += "|" + str(node)
