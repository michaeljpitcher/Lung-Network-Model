#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..EpidemiologyClasses import *
from ..BaseEpidemic.Model.SinglePatchEpidemicModel import *
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

class HethcoteMSEIRModel(SinglePatchEpidemicModel):

    def __init__(self, b, d, beta, delta, epsilon, gamma):
        compartments = [PASSIVELY_IMMUNE, SUSCEPTIBLE, EXPOSED, INFECTIOUS, RECOVERED]

        events = []

        # Birth (immune)
        events.append(CreateByOtherCompartments([Patch], b, PASSIVELY_IMMUNE, [PASSIVELY_IMMUNE, EXPOSED, INFECTIOUS, RECOVERED]))
        # Birth (non-immune)
        events.append(CreateByOtherCompartments([Patch], b, SUSCEPTIBLE, [SUSCEPTIBLE]))

        # Lose immunity
        events.append(Change([Patch], delta, PASSIVELY_IMMUNE, SUSCEPTIBLE))

        # Infect
        events.append(Infect([Patch], beta, SUSCEPTIBLE, EXPOSED, [INFECTIOUS]))

        # Progress to infection
        events.append(Change([Patch], epsilon, EXPOSED, INFECTIOUS))

        # Recover
        events.append(Change([Patch], gamma, INFECTIOUS, RECOVERED))

        # Death
        events.append(Destroy([Patch], d, PASSIVELY_IMMUNE))
        events.append(Destroy([Patch], d, SUSCEPTIBLE))
        events.append(Destroy([Patch], d, EXPOSED))
        events.append(Destroy([Patch], d, INFECTIOUS))
        events.append(Destroy([Patch], d, RECOVERED))

        SinglePatchEpidemicModel.__init__(self, compartments, events)