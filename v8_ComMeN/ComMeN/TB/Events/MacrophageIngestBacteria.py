#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Event import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MacrophageIngestBacteria(Event):

    def __init__(self, probability, macrophage_compartment, bacteria_compartment, macrophage_change_compartment=None,
                 bacteria_change_compartment=None):
        self.macrophage_compartment = macrophage_compartment
        self.bacteria_compartment = bacteria_compartment
        self.macrophage_change_compartment = macrophage_change_compartment
        self.bacteria_change_compartment = bacteria_change_compartment
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.macrophage_compartment] * node.subpopulations[self.bacteria_compartment]

    def update_node(self, node, network):
        node.update_subpopulations(self.bacteria_compartment, -1)

        if self.macrophage_change_compartment is not None:
            node.update_subpopulations(self.macrophage_compartment, -1)
            node.update_subpopulations(self.macrophage_change_compartment, 1)

        if self.bacteria_change_compartment is not None:
            node.update_subpopulations(self.bacteria_change_compartment, 1)
