#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

# imports

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

# Compartments
SUSCEPTIBLE = 'susceptible'
LATENT = 'latent'
NON_INFECTIOUS = 'non_infectious'
INFECTIOUS = 'infectious'
DETECTED = 'detected'
TREATED = 'treated'
RECOVERED = 'recovered'
SUSCEPTIBLE_JUVENILE = 'susceptible_juvenile'
SUSCEPTIBLE_MATURE = 'susceptible_mature'
EXPOSED_JUVENILE = 'exposed_juvenile'
EXPOSED_MATURE = 'exposed_mature'
INFECTIOUS_JUVENILE = 'infected_juvenile'
INFECTIOUS_MATURE = 'infected_mature'
RAT_SUSCEPTIBLE = 'rat_susceptible'
RAT_INFECTIOUS = 'rat_infectious'
RAT_RESISTANT = 'rat_resistant'
FLEA_FREE_INFECTIOUS = 'flea_free_infectious'
AVERAGE_FLEA_ON_RAT = 'average_flea_on_rat'


HICKSON_TOTAL_POPULATION = [SUSCEPTIBLE, LATENT, NON_INFECTIOUS, INFECTIOUS, DETECTED, TREATED]
BLOWER_SIMPLE_TOTAL_POPULATION = [SUSCEPTIBLE, LATENT, INFECTIOUS]
BLOWER_DETAILED_TOTAL_POPULATION = [SUSCEPTIBLE, LATENT, NON_INFECTIOUS, INFECTIOUS, RECOVERED]
FULFORD_TOTAL_POPULATION = [SUSCEPTIBLE_JUVENILE, SUSCEPTIBLE_MATURE, EXPOSED_JUVENILE, EXPOSED_MATURE,
                            INFECTIOUS_JUVENILE, INFECTIOUS_MATURE]

# EDGES
STANDARD_EDGE = 'standard_edge'

# Node Data keys
BIRTH_RATE = 'birth_rate'
DEATH_RATE_JUVENILE = 'death_rate_juvenile'
DEATH_RATE_MATURE = 'death_rate_mature'
AREA = 'area'