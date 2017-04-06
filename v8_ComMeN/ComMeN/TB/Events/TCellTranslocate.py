#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Event import *
from ...Pulmonary.PulmonaryClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TCellTranslocateBronchus(Event):

    def __init__(self, probability, t_cell_compartment, edge_choice_based_on_weight=False):
        self.t_cell_compartment = t_cell_compartment
        self.edge_choice_based_on_weight = edge_choice_based_on_weight
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.t_cell_compartment] * len(network.get_neighbouring_edges(node, BRONCHUS))

    def update_node(self, node, network):
        edges = network.get_neighbouring_edges(node, BRONCHUS)

        chosen_neighbour = None

        # Choose an edge
        if self.edge_choice_based_on_weight:
            total_weight = sum([data[WEIGHT] for _,data in edges])
            r = np.random.random() * total_weight
            running_total = 0
            for (neighbour, data) in edges:
                running_total += data[WEIGHT]
                if running_total > r:
                    chosen_neighbour = neighbour
                    break
        else:
            chosen_neighbour = edges[np.random.randint(0, len(edges))]

        node.update_subpopulation(self.t_cell_compartment, -1)
        chosen_neighbour.update_subpopulation(self.t_cell_compartment, 1)


class TCellTranslocateLymph(Event):

    def __init__(self, t_cell_compartment, probability, direction_only=True):
        self.t_cell_compartment = t_cell_compartment
        self.direction_only = direction_only
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):

        viable_edges = network.get_neighbouring_edges(node, LYMPHATIC_VESSEL)

        if self.direction_only:
            viable_edges = [(n,data) for (n,data) in viable_edges if data[DIRECTION] == n]

        return node.subpopulations[self.t_cell_compartment] * len(viable_edges)

    def update_node(self, node, network):
        viable_edges = network.get_neighbouring_edges(node, BRONCHUS)

        # Choose an edge
        if self.direction_only:
            viable_edges = [(n,data) for (n,data) in viable_edges if data[DIRECTION] == n]

        chosen_neighbour = viable_edges[np.random.randint(0, len(viable_edges))]

        node.update_subpopulation(self.t_cell_compartment, -1)
        chosen_neighbour.update_subpopulation(self.t_cell_compartment, 1)
