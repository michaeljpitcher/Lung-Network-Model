#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..EpidemiologyClasses import *
from ..BaseEpidemic.Model.SinglePatchEpidemicModel import *
from ...Base.Events.Change import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class HethcoteClassicEpidemicModel(SinglePatchEpidemicModel):

    def __init__(self, beta, gamma):
        compartments = [SUSCEPTIBLE, INFECTIOUS, RECOVERED]
        events = []
        # Infect
        events.append(Infect([Patch], beta, SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS]))
        # Recover
        events.append(Change([Patch], gamma, INFECTIOUS, RECOVERED))
        SinglePatchEpidemicModel.__init__(self, compartments, events)