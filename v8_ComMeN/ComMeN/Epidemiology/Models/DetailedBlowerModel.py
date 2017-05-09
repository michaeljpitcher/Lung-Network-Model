#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Network.MetapopulationNetwork import *
from ...Base.Events.Creation import *
from ...Base.Events.Change import *
from ...Base.Events.Destruction import *
from ..EpidemiologyClasses import *
from ..Node.Region import *
import math

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class DetailedBlowerModel(MetapopulationNetwork):

    def __init__(self, population_size, infection_size, pi, p, beta, f, mu, v, q, mu_t, c, omega):
        """
        :param population_size: Amount of susceptibles at start of simulation
        :param pi: Recruitment rate of susceptibles 
        :param p: Proportion of susceptibles infected going to active disease rather than latent
        :param beta: Rate of disease transmission
        :param f: Proportion of susceptibles infected going to active disease that become infectious
        :param mu: Standard death rate
        :param v: Progression rate of latent to active disease
        :param q: Proportion of latent to active disease that become infectious
        :param mu_t: Death rate due to disease
        :param c: Recovery rate 
        :param omega: Relapse rate
        """

        # Events
        # Susceptible recruited
        events = [Create([Region], pi, SUSCEPTIBLE)]
        # Susceptible infected, goes latent
        events.append(ChangeByOtherCompartments([Region], (1 - p) * beta, SUSCEPTIBLE, LATENT, [INFECTIOUS]))
        # Susceptible infected, goes infectious
        events.append(ChangeByOtherCompartments([Region], p * f * beta, SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS]))
        # Susceptible infected, goes non-infectious
        events.append(ChangeByOtherCompartments([Region], p * (1 - f) * beta, SUSCEPTIBLE, NON_INFECTIOUS, [INFECTIOUS]))
        # Susceptible death
        events.append(Destroy([Region], mu, SUSCEPTIBLE))
        # Latent progresses to infectious
        events.append(Change([Region], v * q, LATENT, INFECTIOUS))
        # Latent progresses to non-infectious
        events.append(Change([Region], v * (1 - q), LATENT, NON_INFECTIOUS))
        # Latent death
        events.append(Destroy([Region], mu, LATENT))
        # Infectious dies, standard
        events.append(Destroy([Region], mu, INFECTIOUS))
        # Infectious dies, by disease
        events.append(Destroy([Region], mu_t, INFECTIOUS))
        # Infectious recovers
        events.append(Change([Region], c, INFECTIOUS, RECOVERED))
        # Non-infectious dies, standard
        events.append(Destroy([Region], mu, NON_INFECTIOUS))
        # Non-infectious dies, by disease
        events.append(Destroy([Region], mu_t, NON_INFECTIOUS))
        # Non-infectious recovers
        events.append(Change([Region], c, NON_INFECTIOUS, RECOVERED))
        # Recovered dies
        events.append(Destroy([Region], mu, RECOVERED))
        # Recovered relapses to infectious
        events.append(Change([Region], omega, RECOVERED, INFECTIOUS))
        # Recovered relapses to non-infectious
        events.append(Change([Region], omega, RECOVERED, NON_INFECTIOUS))

        self.population = Region(0, BLOWER_DETAILED_TOTAL_POPULATION)
        self.population.update_subpopulation(SUSCEPTIBLE, population_size-infection_size)
        self.population.update_subpopulation(INFECTIOUS, infection_size)

        MetapopulationNetwork.__init__(self, BLOWER_DETAILED_TOTAL_POPULATION, nodes=[self.population],
                                       edges=[], events=events)

        self.fast_incidence_rate = dict()
        self.slow_incidence_rate = dict()
        self.relapse_incidence_rate = dict()
        self.previous = self.population.subpopulations.copy()

    def timestep_print(self):
        MetapopulationNetwork.timestep_print(self)
        print self.population.subpopulations

        if (self.population.subpopulations[SUSCEPTIBLE] < self.previous[SUSCEPTIBLE]) and \
            (self.population.subpopulations[INFECTIOUS] > self.previous[INFECTIOUS] or
             self.population.subpopulations[NON_INFECTIOUS] > self.previous[NON_INFECTIOUS]):
            interval = math.floor(self.time)
            if interval in self.fast_incidence_rate:
                self.fast_incidence_rate[interval] += 1
            else:
                self.fast_incidence_rate[math.floor(self.time)] = 1
        elif (self.population.subpopulations[LATENT] < self.previous[LATENT]) and \
            (self.population.subpopulations[INFECTIOUS] > self.previous[INFECTIOUS] or
             self.population.subpopulations[NON_INFECTIOUS] > self.previous[NON_INFECTIOUS]):
            interval = math.floor(self.time)
            if interval in self.slow_incidence_rate:
                self.slow_incidence_rate[interval] += 1
            else:
                self.slow_incidence_rate[math.floor(self.time)] = 1
        elif (self.population.subpopulations[RECOVERED] < self.previous[RECOVERED]) and \
            (self.population.subpopulations[INFECTIOUS] > self.previous[INFECTIOUS] or
             self.population.subpopulations[NON_INFECTIOUS] > self.previous[NON_INFECTIOUS]):
            interval = math.floor(self.time)
            if interval in self.relapse_incidence_rate:
                self.relapse_incidence_rate[interval] += 1
            else:
                self.relapse_incidence_rate[math.floor(self.time)] = 1

        self.previous = self.population.subpopulations.copy()
