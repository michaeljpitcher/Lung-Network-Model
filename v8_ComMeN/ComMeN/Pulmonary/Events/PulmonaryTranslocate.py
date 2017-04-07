#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Event import *
from ..PulmonaryClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TranslocateBronchus(Event):

    def __init__(self, probability, translocate_compartment, edge_choice_based_on_weight=False):
        self.translocate_compartment = translocate_compartment
        self.edge_choice_based_on_weight = edge_choice_based_on_weight
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.translocate_compartment] * len(network.get_neighbouring_edges(node, BRONCHUS))

    def choose_neighbour(self, node, network):
        edges = network.get_neighbouring_edges(node, BRONCHUS)
        # Choose an edge
        if self.edge_choice_based_on_weight:
            total_weight = sum([data[WEIGHT] for _, data in edges])
            r = np.random.random() * total_weight
            running_total = 0
            for (neighbour, data) in edges:
                running_total += data[WEIGHT]
                if running_total > r:
                    return neighbour
        else:
            return edges[np.random.randint(0, len(edges))]

    def update_node(self, node, network):
        chosen_neighbour = self.choose_neighbour(node, network)
        translocate(node, chosen_neighbour, self.translocate_compartment)


class TranslocateLymph(Event):

    def __init__(self, probability, translocate_compartment, direction_only=True):
        self.translocate_compartment = translocate_compartment
        self.direction_only = direction_only
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        viable_edges = network.get_neighbouring_edges(node, LYMPHATIC_VESSEL)
        if self.direction_only:
            viable_edges = [(n,data) for (n,data) in viable_edges if data[DIRECTION] == n]
        return node.subpopulations[self.translocate_compartment] * len(viable_edges)

    def choose_neighbour(self, node, network):
        viable_edges = network.get_neighbouring_edges(node, LYMPHATIC_VESSEL)
        # Choose an edge
        if self.direction_only:
            viable_edges = [(n, data) for (n, data) in viable_edges if data[DIRECTION] == n]
        return viable_edges[np.random.randint(0, len(viable_edges))]

    def update_node(self, node, network):
        chosen_neighbour = self.choose_neighbour(node, network)
        translocate(node, chosen_neighbour, self.translocate_compartment)
