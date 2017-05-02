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


def move_internals(node, neighbour, internal_compartment, phagocyte_compartment):
    internal_compartment_amount = node.compartment_per_compartment(internal_compartment, phagocyte_compartment)
    node.update_subpopulation(internal_compartment, -1 * internal_compartment_amount)
    neighbour.update_subpopulation(internal_compartment, internal_compartment_amount)


class TranslocateBronchus(Translocate):

    def __init__(self, node_types, probability, translocate_compartment, internal_compartments=None,
                 edge_choice_based_on_weight=False):
        self.edge_choice_based_on_weight = edge_choice_based_on_weight
        Translocate.__init__(self, node_types, probability, translocate_compartment, BRONCHUS, internal_compartments)

    def choose_neighbour(self, edges):
        # Choose an edge
        if self.edge_choice_based_on_weight:
            total_weight = sum([data[WEIGHT] for _, data in edges])
            r = np.random.random() * total_weight
            running_total = 0
            for (neighbour, data) in edges:
                running_total += data[WEIGHT]
                if running_total >= r:
                    return neighbour
        else:
            return Translocate.choose_neighbour(self, edges)


class TranslocateLymph(Translocate):

    def __init__(self, node_types, probability, translocate_compartment, internal_compartments=None,
                 direction_only=True, flow_based=True):
        self.direction_only = direction_only
        self.flow_based = flow_based
        Translocate.__init__(self, node_types, probability, translocate_compartment, LYMPHATIC_VESSEL,
                             internal_compartments)

    def increment_state_variable_from_node(self, node, network):
        if self.flow_based:
            edges = self.viable_edges(node, network)
            return node.subpopulations[self.translocate_compartment] * sum([data[FLOW_RATE] for _,data in edges])
        else:
            return Translocate.increment_state_variable_from_node(self, node, network)

    def viable_edges(self, node, network):
        # TODO - why is this done every time? more sensible to do once and save somewhere
        if self.direction_only:
            edges = [(n, data) for (n, data) in node.neighbours if data[EDGE_TYPE] == self.edge_type
                     and data[DIRECTION] == n]
        else:
            edges = [(n, data) for (n, data) in node.neighbours if data[EDGE_TYPE] == self.edge_type]
        return edges


class TranslocateBlood(Translocate):

    def __init__(self, node_types, probability, translocate_compartment, internal_compartments=None,
                 direction_only=True):
        self.direction_only = direction_only
        Translocate.__init__(self, node_types, probability, translocate_compartment, HAEMATOGENOUS,
                             internal_compartments)

    def viable_edges(self, node, network):
        if self.direction_only:
            edges = [(n, data) for (n, data) in node.neighbours if data[EDGE_TYPE] == self.edge_type
                     and data[DIRECTION] == n]
        else:
            edges = [(n, data) for (n, data) in node.neighbours if data[EDGE_TYPE] == self.edge_type]
        return edges
