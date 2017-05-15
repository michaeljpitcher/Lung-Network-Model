#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..BaseEpidemic.Model.SinglePatchEpidemicModel import *
from ..EpidemiologyClasses import *
from ...Base.Events.Creation import *
from ...Base.Events.Change import *
from ...Base.Events.Destruction import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class SimpleBlowerModel(SinglePatchEpidemicModel):

    def __init__(self, pi, beta, p, mu, v, mu_t):
        """
        :param population_size: Amount of susceptibles at start of simulation
        :param pi: Recruitment rate of susceptibles 
        :param beta: Rate of disease transmission
        :param p: Proportion of susceptibles infected going to active disease rather than latent
        :param mu: Standard death rate
        :param v: Progression rate of latent to active disease
        :param mu_t: Death rate due to disease
        """

        compartments = [SUSCEPTIBLE, LATENT, INFECTIOUS]

        # Events
        events = []
        # Susceptible birth
        events.append(Create([Patch], pi, SUSCEPTIBLE))
        # Susceptible infected, goes latent
        events.append(ChangeByOtherCompartments([Patch], (1-p)*beta, SUSCEPTIBLE, LATENT, [INFECTIOUS]))
        # Susceptible infected, goes infectious
        events.append(ChangeByOtherCompartments([Patch], p*beta, SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS]))
        # Susceptible death
        events.append(Destroy([Patch], mu, SUSCEPTIBLE))

        # Latent progresses to infectious
        events.append(Change([Patch], v, LATENT, INFECTIOUS))
        # Latent death
        events.append(Destroy([Patch], mu, LATENT))

        # Infectious dies, standard
        events.append(Destroy([Patch], mu, INFECTIOUS))
        # Infectious dies, by disease
        events.append(Destroy([Patch], mu_t, INFECTIOUS))

        SinglePatchEpidemicModel.__init__(self, compartments, events=events)
