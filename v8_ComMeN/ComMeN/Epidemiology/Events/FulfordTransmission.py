#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Change import *
from ..Node.FulfordPatch import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class FulfordTransmission(ChangeByOtherCompartments):

    def __init__(self, compartment_from, compartment_to, influencing_compartments, carrying_capacity,
                 contact_rate_at_carrying_capacity, contact_rate_factor):
        self.c_o = contact_rate_at_carrying_capacity
        self.k = carrying_capacity
        self.epsilon = contact_rate_factor
        ChangeByOtherCompartments.__init__(self, [FulfordPatch], 1, compartment_from, compartment_to,
                                           influencing_compartments)

    def increment_state_variable_from_node(self, node, network):
        p = sum(node.subpopulations.values())
        contact_rate_function = (self.c_o * (p/self.k)) / ((1-self.epsilon) * self.epsilon * (p/self.k))
        return contact_rate_function * ChangeByOtherCompartments.increment_state_variable_from_node(self, node, None)
