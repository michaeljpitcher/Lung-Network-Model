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


class BacteriaReplication(Event):

    def __init__(self, probability, bacteria_compartment):
        self.bacteria_compartment = bacteria_compartment
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.bacteria_compartment]

    def update_node(self, node, network):
        node.update_subpopulation(self.bacteria_compartment, 1)
