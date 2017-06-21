#!/usr/bin/env python

"""Short docstring

S. M. Blower, A. R. Mclean, T. C. Porco, P. M. Small, P. C. Hopewell, M. A. Sanchez, and A. R. Moss, "The intrinsic
transmission dynamics of tuberculosis epidemics," Nat. Med., vol. 1, no. 8, pp. 815-821, Aug. 1995.

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


class DetailedBlowerModel(SinglePatchEpidemicModel):

    def __init__(self, pi, p, beta, f, mu, v, q, mu_t, c, omega):
        """
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

        compartments = [SUSCEPTIBLE, LATENT, INFECTIOUS, NON_INFECTIOUS, RECOVERED]

        # Events
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

        SinglePatchEpidemicModel.__init__(self, compartments, events=events)

        self.fast_incidence_rate = dict()
        self.slow_incidence_rate = dict()
        self.relapse_incidence_rate = dict()
        self.previous = self.node_list[0].subpopulations.copy()

    def timestep_print(self):
        MetapopulationNetwork.timestep_print(self)

        if (self.node_list[0].subpopulations[SUSCEPTIBLE] < self.previous[SUSCEPTIBLE]) and\
           (self.node_list[0].subpopulations[INFECTIOUS] > self.previous[INFECTIOUS] or
             self.node_list[0].subpopulations[NON_INFECTIOUS] > self.previous[NON_INFECTIOUS]):
            interval = math.floor(self.time)
            if interval in self.fast_incidence_rate:
                self.fast_incidence_rate[interval] += 1
            else:
                self.fast_incidence_rate[math.floor(self.time)] = 1
        elif (self.node_list[0].subpopulations[LATENT] < self.previous[LATENT]) and \
            (self.node_list[0].subpopulations[INFECTIOUS] > self.previous[INFECTIOUS] or
             self.node_list[0].subpopulations[NON_INFECTIOUS] > self.previous[NON_INFECTIOUS]):
            interval = math.floor(self.time)
            if interval in self.slow_incidence_rate:
                self.slow_incidence_rate[interval] += 1
            else:
                self.slow_incidence_rate[math.floor(self.time)] = 1
        elif (self.node_list[0].subpopulations[RECOVERED] < self.previous[RECOVERED]) and \
            (self.node_list[0].subpopulations[INFECTIOUS] > self.previous[INFECTIOUS] or
             self.node_list[0].subpopulations[NON_INFECTIOUS] > self.previous[NON_INFECTIOUS]):
            interval = math.floor(self.time)
            if interval in self.relapse_incidence_rate:
                self.relapse_incidence_rate[interval] += 1
            else:
                self.relapse_incidence_rate[math.floor(self.time)] = 1

        self.previous = self.node_list[0].subpopulations.copy()
