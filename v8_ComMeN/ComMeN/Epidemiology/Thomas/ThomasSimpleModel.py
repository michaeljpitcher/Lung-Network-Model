#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..BaseEpidemic.Model.SinglePatchEpidemicModel import *
from ..EpidemiologyClasses import *
from ...Base.Events.Creation import *
from ...Base.Events.Change import *
from ...Base.Events.Destruction import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class SimpleThomasModel(SinglePatchEpidemicModel):

    def __init__(self, b, c_nn, c_ni, beta_n, epsilon_n, p_n, mu_n, mu_nt, nu_n):

        compartments = [SUSCEPTIBLE, LATENT, INFECTIOUS, NON_INFECTIOUS]

        # Events
        events = []

        # Susceptible birth (by all other compartments)
        events.append(CreateByOtherCompartments([Patch], b, SUSCEPTIBLE, compartments))

        # Recovery
        events.append(Change([Patch], c_ni, INFECTIOUS, SUSCEPTIBLE))
        events.append(Change([Patch], c_nn, NON_INFECTIOUS, SUSCEPTIBLE))

        # Infect
        events.append(Infect([Patch], beta_n * (1 - epsilon_n), SUSCEPTIBLE, LATENT, [INFECTIOUS]))
        events.append(Infect([Patch], beta_n * epsilon_n * p_n, SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS]))
        events.append(Infect([Patch], beta_n * epsilon_n * (1 - p_n), SUSCEPTIBLE, NON_INFECTIOUS, [INFECTIOUS]))

        # Deaths
        events.append(Destroy([Patch], mu_n, SUSCEPTIBLE))
        events.append(Destroy([Patch], mu_n, LATENT))
        events.append(Destroy([Patch], mu_nt, INFECTIOUS))
        events.append(Destroy([Patch], mu_nt, NON_INFECTIOUS))

        # Progression
        events.append(Change([Patch], nu_n * p_n, LATENT, INFECTIOUS))
        events.append(Change([Patch], nu_n * (1 - p_n), LATENT, NON_INFECTIOUS))

        SinglePatchEpidemicModel.__init__(self, compartments, events=events)
