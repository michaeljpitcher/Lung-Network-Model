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


class FengTBModel(SinglePatchEpidemicModel):

    def __init__(self, lambda_, mu, beta, c, sigma, k, d, r, p):

        compartments = [SUSCEPTIBLE, LATENT, INFECTIOUS, TREATED]

        events = []

        # Birth (constant recruitment rate)
        events.append(Create([Patch], lambda_, SUSCEPTIBLE))

        # Infection
        events.append(Infect([Patch], beta * c, SUSCEPTIBLE, LATENT, [INFECTIOUS]))
        events.append(Infect([Patch], sigma * beta * c, TREATED, LATENT, [INFECTIOUS]))

        # Exogenous reinfection
        events.append(Infect([Patch], p * beta * c, LATENT, INFECTIOUS, [INFECTIOUS]))

        # Progression
        events.append(Change([Patch], k, LATENT, INFECTIOUS))

        # Death
        for comp in compartments:
            events.append(Destroy([Patch], mu, comp))

        # Treatment
        events.append(Change([Patch], r, INFECTIOUS, TREATED))

        # Death by disease
        events.append(Destroy([Patch], d, INFECTIOUS))



        SinglePatchEpidemicModel.__init__(self, compartments, events)