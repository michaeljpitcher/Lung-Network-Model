#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Base.Events.Destruction import *
from v8_ComMeN.ComMeN.Epidemiology.EpidemiologyClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class KeelingDeathRatSusceptible(Destroy):
    def __init__(self, node_types, d_r):
        Destroy.__init__(self, node_types, d_r, RAT_SUSCEPTIBLE)


class KeelingDeathRatInfectious(Destroy):
    def __init__(self, node_types, probability):
        Destroy.__init__(self, node_types, probability, RAT_INFECTIOUS)

    def update_node(self, node, network):
        Destroy.update_node(self, node, None)
        # Increment free flea TODO - does this need to be rounded?
        node.update_subpopulation(FLEA_FREE_INFECTIOUS, node.subpopulations[FLEA_INDEX])


class KeelingDeathRatInfectiousByInfection(KeelingDeathRatInfectious):
    def __init__(self, node_types, m_r, g_r):
        KeelingDeathRatInfectious.__init__(self, node_types, m_r * (1 - g_r))


class KeelingDeathRatResistant(Destroy):
    def __init__(self, node_types, d_r):
        Destroy.__init__(self, node_types, d_r, RAT_RESISTANT)


class KeelingDeathFreeFlea(Destroy):
    def __init__(self, node_types, d_f):
        Destroy.__init__(self, node_types, d_f, FLEA_FREE_INFECTIOUS)
