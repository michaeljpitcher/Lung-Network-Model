#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from Event import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Destroy(Event):

    def __init__(self, probability, compartment_destroyed):
        self.compartment_destroyed = compartment_destroyed
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.compartment_destroyed]

    def update_node(self, node, network):
        node.update_subpopulation(self.compartment_destroyed, -1)
