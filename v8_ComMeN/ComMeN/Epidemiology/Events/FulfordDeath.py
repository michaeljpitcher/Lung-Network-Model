#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Destruction import *
from ..Node.FulfordPatch import *
from ..EpidemiologyClasses import *


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class FulfordDeath(Destroy):

    def __init__(self, compartment_destroyed, d_1, d_2, zeta, k, theta):
        self.juvenile_death = compartment_destroyed == SUSCEPTIBLE_JUVENILE or \
                              compartment_destroyed == EXPOSED_JUVENILE or \
                              compartment_destroyed == INFECTIOUS_JUVENILE
        self.d_1 = d_1
        self.d_2 = d_2
        self.zeta = zeta
        self.k = k
        self.theta = theta
        Destroy.__init__(self, [FulfordPatch], 1, compartment_destroyed)

    def increment_state_variable_from_node(self, node, network):
        p = sum(node.subpopulations.values())
        if self.juvenile_death:
            death_function = self.d_1 + ((1-self.zeta) * y * (p/self.k)**self.theta)
        else:
            death_function = self.d_2 + (self.zeta * y * (p/self.k)**self.theta)

        return death_function * Destroy.increment_state_variable_from_node(self, node, None)