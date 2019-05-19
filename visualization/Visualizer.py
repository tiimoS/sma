from __future__ import division

from random import sample
from matplotlib import pylab

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as pltc

graph = nx.Graph()


def visualize_network(graph_network, file_name, communities):
    """
    Visualizes the communities by coloring the nodes belonging to the same community in the same color
    :param file_name: name of file to store the graph
    :param communities: list of communities
    :return: matplot showing the network with colored communities
    """
    global graph
    graph = graph_network
    print('Visualizing communities...')
    plt.figure(num=None, figsize=(100, 100), dpi=300)
    plt.axis('off')
    fig = plt.figure(1)
    all_colors = [k for k, v in pltc.cnames.items()]
    colors = sample(all_colors, len(communities))

    i = 0
    pos = nx.spring_layout(graph, iterations=100)
    for community in communities:
        community = [node.key for node in community.total_nodes]
        nx.draw_networkx_nodes(graph, pos, nodelist=community, node_color=colors[i])
        i += 1
    nx.draw_networkx_edges(graph, pos, edge_color='k', width=0.01)
    nx.draw_networkx_labels(graph, pos)

    cut = 1.4
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(-xmax, xmax)
    plt.ylim(-ymax, ymax)

    plt.savefig(file_name, bbox_inches="tight")
    pylab.close()
    del fig
