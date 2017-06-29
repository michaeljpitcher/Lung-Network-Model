#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...PulmonaryVersion2.Network.LobularSingleLungNetwork import *
from ..TBVariables import *
from ...Base.Visuals.MetapopulationNetworkGraph import *
from ...Base.Events.Creation import *
from ...Base.Events.Destruction import *
from ...Base.Events.Translocate import *
from ...Base.Events.Phagocytosis import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TBLobularModel(LobularSingleLungNetwork):

    def __init__(self, alpha, beta, mu_b, mu_m, gamma, k):
        compartments = [BACTERIA, MACROPHAGE, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED, T_CELL]

        events = []
        events.append(Replication([LungLobe], alpha, BACTERIA))
        events.append(Destroy([LungLobe], mu_b, BACTERIA))
        events.append(Translocate([LungLobe], k, BACTERIA, LOBULAR_EDGE))

        events.append(Create([LungLobe], gamma, MACROPHAGE))
        events.append(Phagocytosis([LungLobe], beta, MACROPHAGE, BACTERIA, MACROPHAGE_INFECTED))
        events.append(Destroy([LungLobe], mu_m, MACROPHAGE))

        LobularSingleLungNetwork.__init__(self, compartments, events)


    def draw_network(self):
        draw_network(self, "T", {LungLobe: {NODE_COLOUR: 'red', NODE_SIZE: 2000}},
                 {LOBULAR_EDGE: {EDGE_COLOUR: 'red', EDGE_WIDTH: 5}})
