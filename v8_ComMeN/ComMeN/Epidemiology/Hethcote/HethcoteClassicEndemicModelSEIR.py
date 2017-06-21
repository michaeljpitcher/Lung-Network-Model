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


class HethcoteClassicEndemicModel(SinglePatchEpidemicModel):

    def __init__(self, beta, gamma, mu):
        compartments = [SUSCEPTIBLE, EXPOSED, INFECTIOUS, RECOVERED]
        events = []
        # Infect
        events.append(Infect([Patch], beta, SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS]))
        # Recover
        events.append(Change([Patch], gamma, INFECTIOUS, RECOVERED))

        # Birth
        events.append(CreateByOtherCompartments([Patch], mu, SUSCEPTIBLE, [SUSCEPTIBLE, INFECTIOUS, RECOVERED]))
        # Death
        events.append(Destroy([Patch], mu, SUSCEPTIBLE))
        events.append(Destroy([Patch], mu, INFECTIOUS))
        events.append(Destroy([Patch], mu, RECOVERED))

        SinglePatchEpidemicModel.__init__(self, compartments, events)