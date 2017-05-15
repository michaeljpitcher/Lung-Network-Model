#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..BaseEpidemic.Model.SinglePatchEpidemicModel import *
from ..EpidemiologyClasses import *
from ...Base.Events.Creation import *
from ...Base.Events.Destruction import *
from ...Base.Events.Change import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TBEpidemicModel4(SinglePatchEpidemicModel):

    def __init__(self, beta, gamma, delta, p, q, theta, omega, omega_i):
        compartments = [SUSCEPTIBLE, LATENT, INFECTIOUS, NON_INFECTIOUS]
        events = []

        # Birth
        events.append(CreateByOtherCompartments([Patch], omega, SUSCEPTIBLE, compartments))

        # Death
        events.append(Destroy([Patch], omega, SUSCEPTIBLE))
        events.append(Destroy([Patch], omega, LATENT))
        events.append(Destroy([Patch], omega, INFECTIOUS))
        events.append(Destroy([Patch], omega, NON_INFECTIOUS))

        # Death by infection
        events.append(Destroy([Patch], omega_i, INFECTIOUS))
        events.append(Destroy([Patch], omega_i, NON_INFECTIOUS))

        # Infect
        events.append(Infect([Patch], beta * (1 - p), SUSCEPTIBLE, LATENT, [INFECTIOUS]))
        events.append(Infect([Patch], beta * p * q, SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS]))
        events.append(Infect([Patch], beta * p * (1-q), SUSCEPTIBLE, NON_INFECTIOUS, [INFECTIOUS]))

        # Progression
        events.append(Change([Patch], gamma * q, LATENT, INFECTIOUS))
        events.append(Change([Patch], gamma * (1-q), LATENT, NON_INFECTIOUS))
        # Recovery
        events.append(Change([Patch], delta, INFECTIOUS, SUSCEPTIBLE))
        events.append(Change([Patch], delta, NON_INFECTIOUS, SUSCEPTIBLE))

        # Treatment
        events.append(Change([Patch], theta, INFECTIOUS, SUSCEPTIBLE))
        events.append(Change([Patch], theta, NON_INFECTIOUS, SUSCEPTIBLE))

        SinglePatchEpidemicModel.__init__(self, compartments, events)

    def end_simulation(self):
        # Ends if there's no more chance of infection
        return self.node_list[0].subpopulations[INFECTIOUS] == 0 and self.node_list[0].subpopulations[LATENT] == 0 and \
               self.node_list[0].subpopulations[NON_INFECTIOUS] == 0