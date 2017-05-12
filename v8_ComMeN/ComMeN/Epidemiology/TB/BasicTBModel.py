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


class BasicTBEpidemicModel(SinglePatchEpidemicModel):

    def __init__(self, beta, gamma, delta, omega):
        compartments = [SUSCEPTIBLE, LATENT, INFECTIOUS]
        events = []

        # Birth
        events.append(CreateByOtherCompartments([Patch], omega, SUSCEPTIBLE, compartments))

        # Death
        events.append(Destroy([Patch], omega, SUSCEPTIBLE))
        events.append(Destroy([Patch], omega, LATENT))
        events.append(Destroy([Patch], omega, INFECTIOUS))

        # Infect
        events.append(Infect([Patch], beta, SUSCEPTIBLE, LATENT, [INFECTIOUS]))

        # Progression
        events.append(Change([Patch], gamma, LATENT, INFECTIOUS))
        # Recovery
        events.append(Change([Patch], delta, INFECTIOUS, SUSCEPTIBLE))

        SinglePatchEpidemicModel.__init__(self, compartments, events)
