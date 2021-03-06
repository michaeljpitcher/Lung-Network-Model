#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Change import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class ChangeByOxygen(Change):
    def __init__(self, node_types, probability, compartment_from, compartment_to, oxygen_high_to_change):
        self.oxygen_high_to_change = oxygen_high_to_change
        Change.__init__(self, node_types, probability, compartment_from, compartment_to)

    def increment_state_variable_from_node(self, node, network):
        # TODO - check viability of this method - O2 TENSION IS NOT NECESSARILY BETWEEN 0 AND 1
        if self.oxygen_high_to_change:
            oxygen_factor = node.oxygen_tension
        else:
            oxygen_factor = 1-node.oxygen_tension
        return Change.increment_state_variable_from_node(self, node, network) * oxygen_factor
