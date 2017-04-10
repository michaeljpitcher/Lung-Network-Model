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


class Create(Event):

    def __init__(self, probability, compartment_created):
        self.compartment_created = compartment_created
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return 1

    def update_node(self, node, network):
        node.update_subpopulations(self.compartment_created, 1)


class Replication(Create):

    def __init__(self, probability, compartment_replicating):
        Create.__init__(self, probability, compartment_replicating)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.compartment_created]
