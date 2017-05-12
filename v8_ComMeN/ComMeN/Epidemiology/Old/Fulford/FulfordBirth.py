#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import math

from v8_ComMeN.ComMeN.Epidemiology.Old.Fulford import *

from v8_ComMeN.ComMeN.Base.Events.Creation import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class FulfordBirth(CreateByOtherCompartments):

    def __init__(self, probability, compartment_created, influencing_compartments, k, b, r, delta, theta):
        self.k = k
        self.b = b
        self.r = r
        self.delta = delta
        self.theta = theta
        CreateByOtherCompartments.__init__(self, [FulfordPatch], probability, compartment_created, influencing_compartments)

    def increment_state_variable_from_node(self, node, network):
        p = sum(node.subpopulations.values())
        b_1 = (self.r * self.delta) / (self.b - (self.r * self.delta))
        b_0 = (self.b - (self.r * self.delta)) * math.exp(b_1)
        if p <= self.k:
            birth_function = self.b - (self.r * self.delta * ((p/self.k)**self.theta))
        else:
            birth_function = b_0 * math.exp(-1 * b_1 * ((p/self.k)**self.theta))
        return birth_function * CreateByOtherCompartments.increment_state_variable_from_node(self, node, None)
