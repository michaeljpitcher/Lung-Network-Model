#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from Event import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Translocate(Event):

    def __init__(self, node_types, probability, translocate_compartment, edge_type):
        self.translocate_compartment = translocate_compartment
        self.edge_type = edge_type
        Event.__init__(self, node_types, probability)

    def increment_from_node(self, node, network):
        edges = self.viable_edges(node, network)
        return node.subpopulations[self.translocate_compartment] * len(edges)

    def update_node(self, node, network):
        edges = self.viable_edges(node, network)
        chosen_neighbour = self.choose_neighbour(edges)
        self.move(node, chosen_neighbour)

    def viable_edges(self, node, network):
        return sorted(network.get_neighbouring_edges(node, self.edge_type))

    def choose_neighbour(self, edges):
        return edges[np.random.randint(0, len(edges))][0]

    def move(self, node, neighbour):
        node.update_subpopulation(self.translocate_compartment, -1)
        neighbour.update_subpopulation(self.translocate_compartment, 1)
