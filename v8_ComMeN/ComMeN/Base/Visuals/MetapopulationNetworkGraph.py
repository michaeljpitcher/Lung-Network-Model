#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import matplotlib.pyplot as plt
import networkx as nx
from ..BaseClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

NODE_COLOUR = 'node_color'
NODE_SHAPE = 'node_shape'
NODE_SIZE = 'node_size'
EDGE_WIDTH = 'edge_width'
EDGE_COLOUR = 'edge_color'


def draw_network(network, title, node_formatting, edge_formatting, save_name=None):
    fig = plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.title(title)

    pos = {}

    for n in network.nodes():
        pos[n] = n.position

    for node_type in node_formatting:
        nodes = [n for n in network.nodes() if isinstance(n, node_type)]
        record = node_formatting[node_type]
        if NODE_SHAPE not in record:
            record[NODE_SHAPE] = 'o'
        nx.draw_networkx_nodes(network, nodelist=nodes, pos=pos, node_shape=record[NODE_SHAPE],
                               node_size=record[NODE_SIZE], node_color=record[NODE_COLOUR])

    for edge_type in edge_formatting:
        edges = [(u,v,data) for (u,v,data) in network.edges(data=True) if data[EDGE_TYPE] == edge_type]
        record = edge_formatting[edge_type]
        nx.draw_networkx_edges(network, pos, edgelist=edges, width=record[EDGE_WIDTH], edge_color=record[EDGE_COLOUR])

    plt.show()
    if save_name:
        fig.savefig(save_name + ".png")  # save as png
