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

    def __init__(self, probability, translocate_compartment, edge_type):
        self.translocate_compartment = translocate_compartment
        self.edge_type = edge_type
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.translocate_compartment] * \
               len(network.get_neighbouring_edges(node, self.edge_type))

    def update_node(self, node, network):
        chosen_neighbour = self.choose_neighbour(node, network)
        translocate(node, chosen_neighbour, self.translocate_compartment)

    def choose_neighbour(self, node, network):
        edges = network.get_neighbouring_edges(node, self.edge_type)
        return edges[np.random.randint(0, len(edges))][0]
