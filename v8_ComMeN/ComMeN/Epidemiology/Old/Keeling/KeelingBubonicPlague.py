#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Epidemiology.Old.Keeling.KeelingBirth import *

from v8_ComMeN.ComMeN.Base.Network.MetapopulationNetwork import *
from ..Events.KeelingDeath import *
from ..Events.KeelingInfect import *
from ..Events.KeelingRecover import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class KeelingBubonicPlagueModel(MetapopulationNetwork):

    def __init__(self, r_r, p, k_r, d_r, m_r, g_r, r_f, k_f, d_f, beta_r, a):
        compartments = [RAT_SUSCEPTIBLE, RAT_INFECTIOUS, RAT_RESISTANT, FLEA_FREE_INFECTIOUS, AVERAGE_FLEA_ON_RAT]

        self.a = a

        events = []
        # BIRTHS
        events.append(KeelingRatBirthSusceptibleFromSusceptible([Patch], r_r, k_r))
        events.append(KeelingRatBirthSusceptibleFromResistant([Patch], r_r, p))
        events.append(KeelingRatBirthResistantFromResistant([Patch], r_r, k_r, p))

        events.append(KeelingFleaBirth([Patch], r_f, k_f))

        # DEATHS
        events.append(KeelingDeathRatSusceptible([Patch], d_r))
        events.append(KeelingDeathRatInfectious([Patch], d_r))
        events.append(KeelingDeathRatInfectiousByInfection([Patch], m_r, g_r))
        events.append(KeelingDeathRatResistant([Patch], d_r))

        events.append(KeelingDeathFreeFlea([Patch], d_f))

        # RECOVER
        events.append(KeelingRecover([Patch], m_r, g_r))

        # TRANSMIT
        events.append(KeelingInfect([Patch], beta_r, a))
        events.append(Something([Patch], d_f, a))

        nodes = [Patch(0, compartments)]
        edges = []

        MetapopulationNetwork.__init__(self, compartments, nodes, edges, events)

        self.force_of_infection = dict()

    def timestep_print(self):
        print "t=", self.time
        node = self.node_list[0]
        print node.subpopulations
        t_r = sum([node.subpopulations[n] for n in [RAT_SUSCEPTIBLE, RAT_RESISTANT, RAT_INFECTIOUS]])
        self.force_of_infection[self.time] = node.subpopulations[FLEA_FREE_INFECTIOUS] * math.exp(-1 * self.a * t_r)
        print self.force_of_infection[self.time]