#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Base.Events.Change import *
from v8_ComMeN.ComMeN.Epidemiology.EpidemiologyClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MbahTreatment(Change):
    def __init__(self, node_types, probability):
        Change.__init__(self, node_types, probability, INFECTIOUS, RECOVERED)

    def increment_state_variable_from_node(self, node, network):
        return node.proportion_recieving_treatment * node.subpopulations[INFECTIOUS]
