#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from Event import *
from ..BaseClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Translocate(Event):

    def __init__(self, node_types, probability, translocate_compartment, edge_type, internal_compartments=None):
        self.translocate_compartment = translocate_compartment
        self.edge_type = edge_type
        self.internal_compartments = internal_compartments
        Event.__init__(self, node_types, probability)

    def increment_state_variable_from_node(self, node, network):
        edges = self.viable_edges(node, network)
        return node.subpopulations[self.translocate_compartment] * len(edges)

    def update_node(self, node, network):
        edges = self.viable_edges(node, network)
        chosen_neighbour = self.choose_neighbour(edges)
        self.move(node, chosen_neighbour)

    def viable_edges(self, node, network):
        return [(n, data) for (n, data) in node.neighbours if data[EDGE_TYPE] == self.edge_type]

    def choose_neighbour(self, edges):
        return edges[np.random.randint(0, len(edges))][0]

    def move(self, node, neighbour):
        if self.internal_compartments:
            for c in self.internal_compartments:
                amount_to_move = node.compartment_per_compartment(c, self.translocate_compartment)
                node.update_subpopulation(c, -1 * amount_to_move)
                neighbour.update_subpopulation(c, amount_to_move)
        node.update_subpopulation(self.translocate_compartment, -1)
        neighbour.update_subpopulation(self.translocate_compartment, 1)
