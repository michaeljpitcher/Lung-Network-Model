#!/usr/bin/env python

"""Short docstring

[1] A. L. Lloyd and R. M. May, "Spatial heterogeneity in epidemic models.," J. Theor. Biol., vol. 179, no. 1, pp. 1-11, 
1996.

"""

from .LloydInfect import *
from v8_ComMeN.ComMeN.Epidemiology.BaseEpidemic.Model.MultiPatchFullConnectedEpidemicModel import *
from v8_ComMeN.ComMeN.Epidemiology.EpidemiologyClasses import *
from v8_ComMeN.ComMeN.Base.Events.Creation import *
from v8_ComMeN.ComMeN.Base.Events.Destruction import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class LloydModel(MultiPatchFullConnectedEpidemicModel):

    def __init__(self, number_of_patches, mu, beta, epsilon, sigma, gamma):

        compartments = [SUSCEPTIBLE, EXPOSED, INFECTIOUS, RECOVERED]

        events = []
        # Birth
        events.append(CreateByOtherCompartments([Patch], mu, SUSCEPTIBLE, compartments))
        # Death
        events.append(Destroy([Patch], mu, SUSCEPTIBLE))
        events.append(Destroy([Patch], mu, EXPOSED))
        events.append(Destroy([Patch], mu, INFECTIOUS))
        events.append(Destroy([Patch], mu, RECOVERED))
        # Infect
        # events.append(LloydInfect([Patch], beta, SUSCEPTIBLE, EXPOSED, [INFECTIOUS], epsilon))
        # Progress
        # events.append(Change([Patch], sigma, EXPOSED, INFECTIOUS))

        # Infect
        events.append(LloydInfect([Patch], beta, SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS], epsilon))

        # Recover
        events.append(Change([Patch], gamma, INFECTIOUS, RECOVERED))

        MultiPatchFullConnectedEpidemicModel.__init__(self, number_of_patches, compartments, events)
