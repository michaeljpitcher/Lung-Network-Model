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

    def __init__(self, node_types, probability, compartment_created):
        self.compartment_created = compartment_created
        Event.__init__(self, node_types, probability)

    def increment_state_variable_from_node(self, node, network):
        return 1

    def update_node(self, node, network):
        node.update_subpopulation(self.compartment_created, 1)


class CreateByOtherCompartments(Create):

    def __init__(self, node_types, probability, compartment_created, influencing_compartments):
        self.influencing_compartments = influencing_compartments
        Create.__init__(self, node_types, probability, compartment_created)

    def increment_state_variable_from_node(self, node, network):
        return sum([node.subpopulations[compartment] for compartment in self.influencing_compartments])


class Replication(CreateByOtherCompartments):

    def __init__(self, node_types, probability, compartment_replicating):
        CreateByOtherCompartments.__init__(self, node_types, probability, compartment_replicating, [compartment_replicating])
