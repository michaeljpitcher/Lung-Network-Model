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


# COMPARTMENTS
BACTERIA = 'bacteria'
BACTERIA_FAST = 'bacteria_fast'
BACTERIA_SLOW = 'bacteria_slow'
BACTERIA_INTRACELLULAR = 'bacteria_intracellular'
MACROPHAGE = 'macrophage'
MACROPHAGE_REGULAR = 'macrophage_regular'
MACROPHAGE_INFECTED = 'mcrophage_infected'
MACROPHAGE_ACTIVATED = 'macrophage_activated'
T_CELL = 't_cell'
T_CELL_NAIVE_HELPER = 't_cell_naive_helper'
T_CELL_HELPER = 't_cell_helper'
T_CELL_NAIVE_CYTOTOXIC = 't_cell_naive_cytotoxic'
T_CELL_CYTOTOXIC = 't_cell_cytotoxic'
DENDRITIC_CELL = 'dendritic_cell'
DENDRITIC_CELL_IMMATURE = 'dendritic_cell_immature'
DENDRITIC_CELL_MATURE = 'dendritic_cell_mature'

# Compartments that exude Cytokine
# TODO - treat all cytokine as one
CYTOKINE_PRODUCING_COMPARTMENTS = [MACROPHAGE_INFECTED, T_CELL_HELPER]
