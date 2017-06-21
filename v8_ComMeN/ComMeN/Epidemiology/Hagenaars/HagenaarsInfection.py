#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Change import *
from ..EpidemiologyClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class HagenaarsInfect(Change):

    def __init__(self, node_types, probability, coupling_parameter):
        self.coupling_parameter = coupling_parameter
        Change.__init__(self, node_types, probability, SUSCEPTIBLE, INFECTIOUS)

    def increment_state_variable_from_node(self, node, network):

        # epsilon * sum Ij
        total_neighbour_infectious = self.coupling_parameter * \
                                     sum([neighbour.subpopulations[INFECTIOUS] for (neighbour,data) in node.neighbours])

        # N
        total_at_node = sum(node.subpopulations.values())

        # epsilon(n -1)
        contacts_neighbours = self.coupling_parameter * len(node.neighbours)

        return node.subpopulations[SUSCEPTIBLE] * (node.subpopulations[INFECTIOUS] + total_neighbour_infectious) / \
               (total_at_node * (1 + contacts_neighbours))
