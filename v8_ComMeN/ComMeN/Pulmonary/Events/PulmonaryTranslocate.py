#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Event import *
from ...Base.Events.Translocate import *
from ..PulmonaryClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TranslocateBronchus(Translocate):

    def __init__(self, probability, translocate_compartment, edge_choice_based_on_weight=False):
        self.edge_choice_based_on_weight = edge_choice_based_on_weight
        Translocate.__init__(self, probability, translocate_compartment, BRONCHUS)

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
            return Translocate.choose_neighbour(self, node, network)


class TranslocateLymph(Translocate):

    def __init__(self, probability, translocate_compartment, direction_only=True):
        self.direction_only = direction_only
        Translocate.__init__(self, probability, translocate_compartment, LYMPHATIC_VESSEL)

    def increment_from_node(self, node, network):
        if self.direction_only:
            viable_edges = [(n, data) for (n, data) in network.get_neighbouring_edges(node, LYMPHATIC_VESSEL) if
                            data[DIRECTION] == n]
            return node.subpopulations[self.translocate_compartment] * len(viable_edges)
        else:
            return Translocate.increment_from_node(self, node, network)

    def choose_neighbour(self, node, network):
        if self.direction_only:
            viable_edges = [(neighbour, data) for (neighbour, data) in
                            network.get_neighbouring_edges(node, LYMPHATIC_VESSEL) if data[DIRECTION] == neighbour]
            return viable_edges[np.random.randint(0, len(viable_edges))]
        else:
            return Translocate.choose_neighbour(self, node, network)


class TranslocateBlood(Translocate):

    def __init__(self, probability, translocate_compartment, direction_only=True):
        self.direction_only = direction_only
        Translocate.__init__(self, probability, translocate_compartment, HAEMATOGENOUS)

    def increment_from_node(self, node, network):
        if self.direction_only:
            viable_edges = [(n, data) for (n, data) in network.get_neighbouring_edges(node, HAEMATOGENOUS) if
                            data[DIRECTION] == n]
            return node.subpopulations[self.translocate_compartment] * len(viable_edges)
        else:
            return Translocate.increment_from_node(self, node, network)

    def choose_neighbour(self, node, network):

        if self.direction_only:
            viable_edges = [(neighbour, data) for (neighbour, data) in
                            network.get_neighbouring_edges(node, HAEMATOGENOUS) if data[DIRECTION] == neighbour]
            return viable_edges[np.random.randint(0, len(viable_edges))]
        else:
            return Translocate.choose_neighbour(self, node, network)
