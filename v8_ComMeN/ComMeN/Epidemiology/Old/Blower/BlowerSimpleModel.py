#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Epidemiology.Old.Blower import *

from v8_ComMeN.ComMeN.Base.Events.Change import *
from v8_ComMeN.ComMeN.Base.Events.Creation import *
from v8_ComMeN.ComMeN.Base.Events.Destruction import *
from v8_ComMeN.ComMeN.Base.Network.MetapopulationNetwork import *
from v8_ComMeN.ComMeN.Epidemiology.EpidemiologyClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class SimpleBlowerModel(MetapopulationNetwork):

    def __init__(self, population_size, pi, beta, p, mu, v, mu_t):
        """
        :param population_size: Amount of susceptibles at start of simulation
        :param pi: Recruitment rate of susceptibles 
        :param beta: Rate of disease transmission
        :param p: Proportion of susceptibles infected going to active disease rather than latent
        :param mu: Standard death rate
        :param v: Progression rate of latent to active disease
        :param mu_t: Death rate due to disease
        """

        # Events
        # Susceptible recruited
        events = [Create([Region], pi, SUSCEPTIBLE)]
        # Susceptible infected, goes latent
        events.append(ChangeByOtherCompartments([Region], (1-p)*beta, SUSCEPTIBLE, LATENT, [INFECTIOUS]))
        # Susceptible infected, goes infectious
        events.append(ChangeByOtherCompartments([Region], p*beta, SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS]))
        # Susceptible death
        events.append(Destroy([Region], mu, SUSCEPTIBLE))
        # Latent progresses to infectious
        events.append(Change([Region], v, LATENT, INFECTIOUS))
        # Latent death
        events.append(Destroy([Region], mu, LATENT))
        # Infectious dies, standard
        events.append(Destroy([Region], mu, INFECTIOUS))
        # Infectious dies, by disease
        events.append(Destroy([Region], mu_t, INFECTIOUS))

        self.node = Region(0, BLOWER_SIMPLE_TOTAL_POPULATION)
        self.node.update_subpopulation(SUSCEPTIBLE, population_size)

        MetapopulationNetwork.__init__(self, BLOWER_SIMPLE_TOTAL_POPULATION, nodes=[self.node],
                                       edges=[], events=events)
