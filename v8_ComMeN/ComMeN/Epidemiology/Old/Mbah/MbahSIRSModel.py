#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Epidemiology.Old.Mbah import *

from v8_ComMeN.ComMeN.Base.Events.Creation import *
from v8_ComMeN.ComMeN.Base.Events.Destruction import *
from v8_ComMeN.ComMeN.Base.Network.MetapopulationNetwork import *
from ..Events.MbahTreatment import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MbahSIRSModel(MetapopulationNetwork):

    def __init__(self, sigma, mu, nu, eta, beta, epsilon, f0, f1):

        compartments = [SUSCEPTIBLE, INFECTIOUS, RECOVERED]

        nodes = [MbahPatch(0, compartments, f0), MbahPatch(1, compartments, f1)]

        edges = [(nodes[0], nodes[1], {EDGE_TYPE:'edge'})]

        # Events
        events = []
        # Birth
        events.append(CreateByOtherCompartments([MbahPatch], sigma, SUSCEPTIBLE, compartments))

        # Death
        events.append(Destroy([MbahPatch], sigma, SUSCEPTIBLE))
        events.append(Destroy([MbahPatch], sigma, INFECTIOUS))
        events.append(Destroy([MbahPatch], sigma, RECOVERED))

        # Recover with immunity (I -> R)
        events.append(Change([MbahPatch], mu, INFECTIOUS, RECOVERED))

        # Immunity wears off (R -> S)
        events.append(Change([MbahPatch], nu, RECOVERED, SUSCEPTIBLE))

        # Treatment
        events.append(MbahTreatment([MbahPatch], eta))

        # Infect
        events.append(MbahInfectWithinPatch([MbahPatch], beta, epsilon))
        events.append(MbahInfectAcrossPatch([MbahPatch], beta, epsilon))

        MetapopulationNetwork.__init__(self, compartments, nodes=nodes, edges=edges, events=events)
