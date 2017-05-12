#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import csv

import matplotlib.pyplot as plt

from v8_ComMeN.ComMeN.Epidemiology.Hethcote.HethcoteClassicEpidemicModel import *
from v8_ComMeN.ComMeN.Epidemiology.Hethcote.HethcoteClassicEndemicModel import *
from v8_ComMeN.ComMeN.Epidemiology.BaseEpidemic.Graphing.PopulationGraph import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def model_2_3_epidemic():
    sigma = 3
    infectious_period = 3
    gamma = 1.0/infectious_period
    beta = sigma * gamma
    model = HethcoteClassicEpidemicModel(beta, gamma)
    model.seed_network_node_id(0, {SUSCEPTIBLE:990, INFECTIOUS:10})
    run_id = 1
    model.run(35, run_id=run_id)
    draw_population_graph(run_id, model.compartments, "HETHCOTE CLASSIC EPIDEMIC")


def model_2_4_endemic():
    sigma = 3
    infectious_period = 3
    gamma = 1.0 / infectious_period
    beta = sigma * gamma
    mu = 0.05
    model = HethcoteClassicEndemicModel(beta, gamma, mu)
    model.seed_network_node_id(0, {SUSCEPTIBLE: 990, INFECTIOUS: 10})
    run_id = 1
    model.run(500, run_id=run_id)
    draw_population_graph(run_id, model.compartments, "HETHCOTE CLASSIC ENDEMIC")

model_2_3_epidemic()
# model_2_4_endemic()