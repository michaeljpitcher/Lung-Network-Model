#!/usr/bin/env python

"""Short docstring

Basically Blower detailed, but allows migration

"""

from ..BaseEpidemic.Model.MultiPatchFullConnectedEpidemicModel import *
from ...Base.Events.Creation import *
from ...Base.Events.Change import *
from ...Base.Events.Destruction import *
from ...Base.Events.Translocate import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TBEpidemicModel6(MultiPatchFullConnectedEpidemicModel):

    def __init__(self, number_of_patches, pi, p, beta, f, mu, v, q, mu_t, c, omega, g, g_i):

        compartments = [SUSCEPTIBLE, LATENT, INFECTIOUS, NON_INFECTIOUS, RECOVERED]

        events = []
        # Susceptible recruited
        events.append(Create([Patch], pi, SUSCEPTIBLE))
        # Susceptible infected, goes latent
        events.append(ChangeByOtherCompartments([Patch], (1 - p) * beta, SUSCEPTIBLE, LATENT, [INFECTIOUS]))
        # Susceptible infected, goes infectious
        events.append(ChangeByOtherCompartments([Patch], p * f * beta, SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS]))
        # Susceptible infected, goes non-infectious
        events.append(ChangeByOtherCompartments([Patch], p * (1 - f) * beta, SUSCEPTIBLE, NON_INFECTIOUS, [INFECTIOUS]))
        # Susceptible death
        events.append(Destroy([Patch], mu, SUSCEPTIBLE))
        # Latent progresses to infectious
        events.append(Change([Patch], v * q, LATENT, INFECTIOUS))
        # Latent progresses to non-infectious
        events.append(Change([Patch], v * (1 - q), LATENT, NON_INFECTIOUS))
        # Latent death
        events.append(Destroy([Patch], mu, LATENT))
        # Infectious dies, standard
        events.append(Destroy([Patch], mu, INFECTIOUS))
        # Infectious dies, by disease
        events.append(Destroy([Patch], mu_t, INFECTIOUS))
        # Infectious recovers
        events.append(Change([Patch], c, INFECTIOUS, RECOVERED))
        # Non-infectious dies, standard
        events.append(Destroy([Patch], mu, NON_INFECTIOUS))
        # Non-infectious dies, by disease
        events.append(Destroy([Patch], mu_t, NON_INFECTIOUS))
        # Non-infectious recovers
        events.append(Change([Patch], c, NON_INFECTIOUS, RECOVERED))
        # Recovered dies
        events.append(Destroy([Patch], mu, RECOVERED))
        # Recovered relapses to infectious
        events.append(Change([Patch], omega, RECOVERED, INFECTIOUS))
        # Recovered relapses to non-infectious
        events.append(Change([Patch], omega, RECOVERED, NON_INFECTIOUS))

        # Movement
        events.append(Translocate([Patch], g, SUSCEPTIBLE, STANDARD_EDGE, False))
        events.append(Translocate([Patch], g, LATENT, STANDARD_EDGE, False))
        events.append(Translocate([Patch], g_i, INFECTIOUS, STANDARD_EDGE, False))
        events.append(Translocate([Patch], g_i, NON_INFECTIOUS, STANDARD_EDGE, False))
        events.append(Translocate([Patch], g, RECOVERED, STANDARD_EDGE, False))

        MultiPatchFullConnectedEpidemicModel.__init__(self, number_of_patches, compartments, events)