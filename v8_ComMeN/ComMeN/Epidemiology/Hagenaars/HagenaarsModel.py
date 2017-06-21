#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..BaseEpidemic.Model.MultiPatchFullConnectedEpidemicModel import *
from ..EpidemiologyClasses import *
from HagenaarsInfection import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class HagenaarsModel(MultiPatchFullConnectedEpidemicModel):

    def __init__(self, number_patches, mu, beta, epsilon, nu):

        compartments = [SUSCEPTIBLE, INFECTIOUS, RECOVERED]

        events = []
        # TODO - birth death migration?

        # Infection
        events.append(HagenaarsInfect([Patch], beta, epsilon))

        # Recovery
        events.append(Change([Patch], nu, INFECTIOUS, RECOVERED))

        MultiPatchFullConnectedEpidemicModel.__init__(self, number_patches, compartments, events)