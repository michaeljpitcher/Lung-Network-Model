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


class TBEpidemicModel5(SinglePatchEpidemicModel):

    def __init__(self, beta, gamma, delta, p, q, omicron, theta, omega, omega_i):
        compartments = [SUSCEPTIBLE, LATENT, INFECTIOUS, NON_INFECTIOUS, TREATED, INFECTIOUS_RESISTANT]
        events = []

        # Birth
        events.append(CreateByOtherCompartments([Patch], omega, SUSCEPTIBLE, compartments))

        # Death
        events.append(Destroy([Patch], omega, SUSCEPTIBLE))
        events.append(Destroy([Patch], omega, LATENT))
        events.append(Destroy([Patch], omega, INFECTIOUS))
        events.append(Destroy([Patch], omega, NON_INFECTIOUS))
        events.append(Destroy([Patch], omega, TREATED))
        events.append(Destroy([Patch], omega, INFECTIOUS_RESISTANT))

        # Death by infection
        events.append(Destroy([Patch], omega_i, INFECTIOUS))
        events.append(Destroy([Patch], omega_i, NON_INFECTIOUS))
        events.append(Destroy([Patch], omega_i, INFECTIOUS_RESISTANT))

        # Infect
        events.append(Infect([Patch], beta * (1 - p), SUSCEPTIBLE, LATENT, [INFECTIOUS]))
        events.append(Infect([Patch], beta * p * q, SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS]))
        events.append(Infect([Patch], beta * p * (1-q), SUSCEPTIBLE, NON_INFECTIOUS, [INFECTIOUS]))

        events.append(Infect([Patch], beta * q, SUSCEPTIBLE, INFECTIOUS_RESISTANT, [INFECTIOUS_RESISTANT]))

        # Progression
        events.append(Change([Patch], gamma * q, LATENT, INFECTIOUS))
        events.append(Change([Patch], gamma * (1-q), LATENT, NON_INFECTIOUS))

        # Recovery
        events.append(Change([Patch], delta, INFECTIOUS, SUSCEPTIBLE))
        events.append(Change([Patch], delta, NON_INFECTIOUS, SUSCEPTIBLE))

        # Treatment
        events.append(Change([Patch], theta, INFECTIOUS, TREATED))
        events.append(Change([Patch], theta, NON_INFECTIOUS, TREATED))

        # Treatment recovery
        events.append(Change([Patch], (1-omicron), TREATED, SUSCEPTIBLE))
        # Treatment non-adherence
        events.append(Change([Patch], omicron, TREATED, INFECTIOUS_RESISTANT))

        SinglePatchEpidemicModel.__init__(self, compartments, events)

    def end_simulation(self):
        # Ends if there's no more chance of infection
        return self.node_list[0].subpopulations[INFECTIOUS] == 0 and self.node_list[0].subpopulations[LATENT] == 0 and \
               self.node_list[0].subpopulations[NON_INFECTIOUS] == 0 and self.node_list[0].subpopulations[INFECTIOUS_RESISTANT] == 0