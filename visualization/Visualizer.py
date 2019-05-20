from __future__ import division

from random import sample
from matplotlib import pylab

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as pltc

graph = nx.Graph()
pos = nx.spring_layout(graph, iterations=100)


def visualize_network(graph_network, file_name, communities, path, edge_color):
    """
    Visualizes communities and potential paths of the network.

    :param graph_network: graph of network to be visualized - networkx
    :param file_name: name of output file with the visualization
    :param communities: list of communities to be colored
    :param path: potential paths that should be colored
    :param edge_color: color of potential paths to be used
    :return: graph visualization including colored communities and colored paths.
    """
    global graph, pos
    graph = graph_network

    print('Visualizing Network...')
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

    if len(path) > 0:
        edge_list = []
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            edge_list.append(edge)
        nx.draw_networkx_edges(graph, pos, edgelist=edge_list, edge_color=edge_color, width=0.1)

    cut = 1.4
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(-xmax, xmax)
    plt.ylim(-ymax, ymax)

    plt.savefig(file_name, bbox_inches="tight")
    pylab.close()
    del fig
    print('Finished visualization, saved as ', file_name, '\n')
