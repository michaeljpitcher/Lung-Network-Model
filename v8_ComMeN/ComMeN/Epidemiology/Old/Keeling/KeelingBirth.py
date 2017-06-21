#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Base.Events.Creation import *
from v8_ComMeN.ComMeN.Epidemiology.EpidemiologyClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class KeelingRatBirthSusceptibleFromSusceptible(Create):
    def __init__(self, node_types, r_r, k_r):
        self.carrying_capacity = k_r
        Create.__init__(self, node_types, r_r, RAT_SUSCEPTIBLE)

    def increment_state_variable_from_node(self, node, network):
        t_r = sum([node.subpopulations[c] for c in (RAT_SUSCEPTIBLE, RAT_INFECTIOUS, RAT_RESISTANT)])
        return node.subpopulations[RAT_SUSCEPTIBLE] * (1 - (t_r / self.carrying_capacity))


class KeelingRatBirthSusceptibleFromResistant(Create):
    def __init__(self, node_types, r_r, p):
        self.p = p
        Create.__init__(self, node_types, r_r * (1 - p), RAT_SUSCEPTIBLE)

    def increment_state_variable_from_node(self, node, network):
        return node.subpopulations[RAT_RESISTANT]


class KeelingRatBirthResistantFromResistant(Create):
    def __init__(self, node_types, r_r, k_r, p):
        self.p = p
        self.carrying_capacity = k_r
        Create.__init__(self, node_types, r_r, RAT_RESISTANT)

    def increment_state_variable_from_node(self, node, network):
        t_r = sum([node.subpopulations[c] for c in (RAT_SUSCEPTIBLE, RAT_INFECTIOUS, RAT_RESISTANT)])
        return node.subpopulations[RAT_RESISTANT] * (self.p - (t_r / self.carrying_capacity))


class KeelingFleaBirth(Create):
    def __init__(self, node_types, r_f, k_f):
        self.k_f = k_f
        Create.__init__(self, node_types, r_f, FLEA_INDEX)

    def increment_state_variable_from_node(self, node, network):
        return node.subpopulations[FLEA_INDEX] * (1 - (node.subpopulations[FLEA_INDEX] / self.k_f))
