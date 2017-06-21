#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Base.Events.Change import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class LloydInfect(ChangeByOtherCompartments):
    """
    From "3.1 A SYMMETRIC SPECIAL CASE" - assumes rate of contact is beta within the node (which is passed in as the 
    event probability) and epsilon * beta between nodes
    """

    def __init__(self, node_types, probability, compartment_from, compartment_to, infectious_compartments,
                 coupling_parameter):
        self.coupling_parameter = coupling_parameter
        ChangeByOtherCompartments.__init__(self, node_types, probability, compartment_from, compartment_to,
                                           infectious_compartments)

    def increment_state_variable_from_node(self, node, network):
        total = sum([node.subpopulations[n] for n in self.influencing_compartments])
        for (neighbour, edge) in node.neighbours:
            total += self.coupling_parameter * sum([neighbour.subpopulations[n] for n in self.influencing_compartments])
        return total * node.subpopulations[self.compartment_from]
