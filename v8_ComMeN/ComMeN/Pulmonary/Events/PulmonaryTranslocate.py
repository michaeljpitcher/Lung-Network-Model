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

    def __init__(self, node_types, probability, translocate_compartment, edge_choice_based_on_weight=False):
        self.edge_choice_based_on_weight = edge_choice_based_on_weight
        Translocate.__init__(self, node_types, probability, translocate_compartment, BRONCHUS)

    def choose_neighbour(self, edges):
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
            return Translocate.choose_neighbour(self, edges)


class TranslocateLymph(Translocate):

    def __init__(self, node_types, probability, translocate_compartment, direction_only=True):
        self.direction_only = direction_only
        Translocate.__init__(self, node_types, probability, translocate_compartment, LYMPHATIC_VESSEL)

    def viable_edges(self, node, network):
        edges = Translocate.viable_edges(self, node, network)
        if self.direction_only:
            edges = [(n, data) for (n, data) in edges if data[DIRECTION] == n]
        return edges


class TranslocateBlood(Translocate):

    def __init__(self, node_types, probability, translocate_compartment, direction_only=True):
        self.direction_only = direction_only
        Translocate.__init__(self, node_types, probability, translocate_compartment, HAEMATOGENOUS)

    def viable_edges(self, node, network):
        edges = Translocate.viable_edges(self, node, network)
        if self.direction_only:
            edges = [(n, data) for (n, data) in edges if data[DIRECTION] == n]
        return edges
