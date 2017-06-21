#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Base.Events.Change import *
from v8_ComMeN.ComMeN.Epidemiology.EpidemiologyClasses import *
from v8_ComMeN.ComMeN.Base.Events.Creation import *
import math

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class KeelingInfect(Change):
    def __init__(self, node_types, beta_r, a):
        self.a = a
        Change.__init__(self, node_types, beta_r, RAT_SUSCEPTIBLE, RAT_INFECTIOUS)

    def increment_state_variable_from_node(self, node, network):
        t_r = sum([node.subpopulations[n] for n in [RAT_INFECTIOUS, RAT_SUSCEPTIBLE, RAT_RESISTANT]])
        return (node.subpopulations[RAT_SUSCEPTIBLE] / t_r) * node.subpopulations[FLEA_FREE_INFECTIOUS] * \
               (1 - math.exp(-1 * self.a * t_r))


class Something(Create):
    def __init__(self, node_types, d_f, a):
        self.a = a
        Create.__init__(self, node_types, d_f, FLEA_INDEX)

    def increment_state_variable_from_node(self, node, network):
        t_r = sum([node.subpopulations[n] for n in [RAT_INFECTIOUS, RAT_SUSCEPTIBLE, RAT_RESISTANT]])
        return (1 / t_r) * node.subpopulations[FLEA_FREE_INFECTIOUS] * (1 - math.exp(-1 * self.a * t_r))
