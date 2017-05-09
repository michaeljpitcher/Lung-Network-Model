#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Network.MetapopulationNetwork import *
from ..Node.FulfordPatch import *
from ..EpidemiologyClasses import *
from ..Events.FulfordBirth import *
from ..Events.FulfordDeath import *
from ..Events.FulfordTransmission import *
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

    def __init__(self, patch_data, edge_data, beta_nu, sigma, alpha, a, z, s, k, b, r, delta, theta, c_o, epsilon):

        patches = []
        for n in patch_data.keys():
            birth_rate = patch_data[n][BIRTH_RATE]
            death_rate_juvenile = patch_data[n][DEATH_RATE_JUVENILE]
            death_rate_mature = patch_data[n][DEATH_RATE_MATURE]
            area = patch_data[n][AREA]
            patches.append(FulfordPatch(n, FULFORD_TOTAL_POPULATION, area=area, birth_rate=birth_rate,
                                        death_rate_juvenile=death_rate_juvenile, death_rate_mature=death_rate_mature))

        edges = []
        if len(patch_data) > 1:
            # TODO - edges
            pass

        # EVENTS
        events = []

        # BIRTH
        # TODO - check the derivation of this is correct
        # Susceptible births from non-infectious mothers
        events.append(FulfordBirth(1, SUSCEPTIBLE_JUVENILE, [SUSCEPTIBLE_MATURE, EXPOSED_MATURE], k, b, r, delta, theta))
        # Susceptible births from infectious mothers
        events.append(FulfordBirth((1 - beta_nu), SUSCEPTIBLE_JUVENILE, [INFECTIOUS_MATURE], k, b, r, delta, theta))
        # Exposed births from infectious mothers
        events.append(FulfordBirth(beta_nu, EXPOSED_JUVENILE, [INFECTIOUS_MATURE], k, b, r, delta, theta))

        # Transmission
        # TODO - do we need to worry about total pop?
        events.append(FulfordTransmission(SUSCEPTIBLE_JUVENILE, EXPOSED_JUVENILE, [INFECTIOUS_JUVENILE],
                                          carrying_capacity=k, contact_rate_at_carrying_capacity=c_o,
                                          contact_rate_factor=epsilon))
        events.append(FulfordTransmission(SUSCEPTIBLE_JUVENILE, EXPOSED_JUVENILE, [INFECTIOUS_MATURE],
                                          carrying_capacity=k, contact_rate_at_carrying_capacity=c_o,
                                          contact_rate_factor=epsilon))
        events.append(FulfordTransmission(SUSCEPTIBLE_MATURE, EXPOSED_MATURE, [INFECTIOUS_JUVENILE],
                                          carrying_capacity=k, contact_rate_at_carrying_capacity=c_o,
                                          contact_rate_factor=epsilon))
        events.append(FulfordTransmission(SUSCEPTIBLE_MATURE, EXPOSED_MATURE, [INFECTIOUS_MATURE],
                                          carrying_capacity=k, contact_rate_at_carrying_capacity=c_o,
                                          contact_rate_factor=epsilon))

        # PROGRESSION
        events.append(Change([FulfordPatch], sigma, EXPOSED_JUVENILE, INFECTIOUS_JUVENILE))
        events.append(Change([FulfordPatch], sigma, EXPOSED_MATURE, INFECTIOUS_MATURE))

        # MATURATION
        # TODO - how does patch area play into this?
        # Susceptible matures on own patch
        events.append(Change([FulfordPatch], a * (1 - z), SUSCEPTIBLE_JUVENILE, SUSCEPTIBLE_MATURE))
        # Exposed matures on own patch
        events.append(Change([FulfordPatch], a * (1 - z), EXPOSED_JUVENILE, EXPOSED_MATURE))
        # Infectious matures on patch
        events.append(Change([FulfordPatch], a, INFECTIOUS_JUVENILE, INFECTIOUS_MATURE))

        if len(patch_data) > 1:
            # Susceptible migrates but is unsuccessful (dies)
            events.append(Destroy([FulfordPatch], a * z * (1 - s), SUSCEPTIBLE_JUVENILE))
            # Susceptible migrates and is successful, so matures
            events.append(TranslocateAndChange([FulfordPatch], a * z * s, SUSCEPTIBLE_JUVENILE, STANDARD_EDGE,
                                           SUSCEPTIBLE_MATURE, probability_increases_with_edges=False))
            # Exposed migrates but is unsuccessful (dies)
            events.append(Destroy([FulfordPatch], a * z * (1 - s), EXPOSED_JUVENILE))
            # Exposed migrates and is successful, so matures
            events.append(TranslocateAndChange([FulfordPatch], a * z * s, EXPOSED_JUVENILE, STANDARD_EDGE,
                                               EXPOSED_MATURE, probability_increases_with_edges=False))

        # DEATH
        # Susceptible juvenile death
        events.append(FulfordDeath(SUSCEPTIBLE_JUVENILE))
        # Exposed juvenile death
        events.append(FulfordDeath(EXPOSED_JUVENILE))
        # Infectious juvenile death
        events.append(FulfordDeath(INFECTIOUS_JUVENILE))
        # Susceptible mature death
        events.append(FulfordDeath(SUSCEPTIBLE_MATURE))
        # Exposed mature death
        events.append(FulfordDeath(EXPOSED_MATURE))
        # Infectious mature death
        events.append(FulfordDeath(INFECTIOUS_MATURE))
        # Death by TB
        events.append(Destroy([FulfordPatch], alpha, INFECTIOUS_JUVENILE))
        events.append(Destroy([FulfordPatch], alpha, INFECTIOUS_MATURE))

        MetapopulationNetwork.__init__(self, FULFORD_TOTAL_POPULATION, patches, edges, events)
