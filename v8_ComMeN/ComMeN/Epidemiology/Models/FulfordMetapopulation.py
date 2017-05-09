#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Network.MetapopulationNetwork import *
from ...Base.Node.Patch import *
from ..EpidemiologyClasses import *
from ...Base.Events.Creation import *
from ...Base.Events.Destruction import *
from ...Base.Events.Change import *
from ...Base.Events.Translocate import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"





class FulfordMetapopultionModel(MetapopulationNetwork):

    def __init__(self, number_patches, b, d, beta_nu, sigma, alpha, a):

        patches = []
        for n in range(number_patches):
            patches.append(Patch(n, FULFORD_TOTAL_POPULATION))

        # EVENTS
        events = []

        # BIRTH
        # TODO - check the derivation of this is correct
        # Susceptible births from non-infectious mothers
        events.append(CreateByOtherCompartments([Patch], b, SUSCEPTIBLE_JUVENILE, [SUSCEPTIBLE_MATURE, EXPOSED_MATURE]))
        # Susceptible births from infectious mothers
        events.append(CreateByOtherCompartments([Patch], b * (1 - beta_nu), SUSCEPTIBLE_JUVENILE, [INFECTIOUS_MATURE]))
        # Exposed births from infectious mothers
        events.append(CreateByOtherCompartments([Patch], b * beta_nu, EXPOSED_JUVENILE, [INFECTIOUS_MATURE]))

        # PROGRESSION
        events.append(Change([Patch], sigma, EXPOSED_JUVENILE, INFECTIOUS_JUVENILE))
        events.append(Change([Patch], sigma, EXPOSED_MATURE, INFECTIOUS_MATURE))

        # MATURATION
        # Susceptible migrates and matures

        # Susceptible matures on patch
        events.append(Change([Patch], ?, SUSCEPTIBLE_JUVENILE, SUSCEPTIBLE_MATURE))
        # Exposed migrates and matures

        # Exposed matures on patch
        events.append(Change([Patch], ?, EXPOSED_JUVENILE, EXPOSED_MATURE))
        # Infectious matures on patch
        events.append(Change([Patch], ?, INFECTIOUS_JUVENILE, INFECTIOUS_MATURE))

        # DEATH
        # Susceptible juvenile death
        events.append(Destroy([Patch], d, SUSCEPTIBLE_JUVENILE))
        # Exposed juvenile death
        events.append(Destroy([Patch], d, EXPOSED_JUVENILE))
        # Infectious juvenile death
        events.append(Destroy([Patch], d, INFECTIOUS_JUVENILE))
        # Susceptible mature death
        events.append(Destroy([Patch], d, SUSCEPTIBLE_MATURE))
        # Exposed mature death
        events.append(Destroy([Patch], d, EXPOSED_MATURE))
        # Infectious mature death
        events.append(Destroy([Patch], d, INFECTIOUS_MATURE))
        # Death by TB
        events.append(Destroy([Patch], alpha, INFECTIOUS_JUVENILE))
        events.append(Destroy([Patch], alpha, INFECTIOUS_MATURE))

        MetapopulationNetwork.__init__(self, FULFORD_TOTAL_POPULATION, patches, edges, events)
