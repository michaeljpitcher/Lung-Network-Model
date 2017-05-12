#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Epidemiology.Old.Mbah import *

from v8_ComMeN.ComMeN.Base.Events.Change import *
from v8_ComMeN.ComMeN.Epidemiology.EpidemiologyClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MbahInfectWithinPatch(Change):
    def __init__(self, node_types, probability, epsilon):
        self.epsilon = epsilon
        Change.__init__(self, node_types, probability, SUSCEPTIBLE, INFECTIOUS)

    def increment_state_variable_from_node(self, node, network):
        N = sum(node.subpopulations.values())
        if N == 0:
            return 0
        else:
            return (1 - self.epsilon) * node.subpopulations[SUSCEPTIBLE] * node.subpopulations[INFECTIOUS] / N


class MbahInfectAcrossPatch(Change):
    def __init__(self, node_types, probability, epsilon):
        self.epsilon = epsilon
        Change.__init__(self, node_types, probability, SUSCEPTIBLE, INFECTIOUS)

    def increment_state_variable_from_node(self, node, network):
        neighbour = node.neighbours[0][0]
        assert isinstance(neighbour, MbahPatch)
        # TODO - is N pop of node or neighbour? Paper assumes they're the same
        N = sum(node.subpopulations.values())
        if N == 0:
            return 0
        else:
            return self.epsilon * node.subpopulations[SUSCEPTIBLE] * neighbour.subpopulations[INFECTIOUS] / N