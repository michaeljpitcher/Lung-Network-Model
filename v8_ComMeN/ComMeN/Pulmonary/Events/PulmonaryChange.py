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


class ChangeByOxygen(Event):
    def __init__(self, probability, compartment_from, compartment_to, oxygen_high_to_change):
        self.compartment_from = compartment_from
        self.compartment_to = compartment_to
        self.oxygen_high_to_change = oxygen_high_to_change
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        if self.oxygen_high_to_change:
            return node.oxygen_tension
        else:
            return 1 / node.oxygen_tension

    def update_node(self, node, network):
        change(node, self.compartment_from, self.compartment_to)
