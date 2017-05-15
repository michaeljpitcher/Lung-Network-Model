#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import csv

import matplotlib.pyplot as plt

from v8_ComMeN.ComMeN.Epidemiology.Hethcote.HethcoteClassicEpidemicModel import *
from v8_ComMeN.ComMeN.Epidemiology.Hethcote.HethcoteClassicEndemicModel import *
from v8_ComMeN.ComMeN.Epidemiology.Hethcote.HethcoteMSEIRModel import *
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
    model.seed_network_node_id(0, {SUSCEPTIBLE:10000*(1-0.01), INFECTIOUS:10000*(0.01)})
    run_id = 1
    model.run(25, run_id=run_id)
    draw_population_graph(run_id, model.compartments, title="HETHCOTE CLASSIC EPIDEMIC")


def model_2_4_endemic():
    gamma = 1.0 / 3
    beta = 1
    mu = 0.1
    model = HethcoteClassicEndemicModel(beta, gamma, mu)
    model.seed_network_node_id(0, {SUSCEPTIBLE: 10000*(1-0.01), INFECTIOUS:10000*(0.01)})
    run_id = 1
    model.run(50, run_id=run_id)
    draw_population_graph(run_id, model.compartments, title="HETHCOTE CLASSIC ENDEMIC")


def model_3_1_MSEIR():
    b = 0.1
    d = 0.095
    beta = 3
    delta = 0.1
    epsilon = 2
    gamma = 0.01
    model = HethcoteMSEIRModel(b=b, d=d, beta=beta, delta=delta, epsilon=epsilon, gamma=gamma)
    model.seed_network_node_id(0, {SUSCEPTIBLE: 10000 * (1 - 0.01), INFECTIOUS: 10000 * (0.01)})
    run_id = 1
    model.run(50, run_id=run_id)
    draw_population_graph(run_id, model.compartments, title="HETHCOTE MSEIR")


# model_2_3_epidemic()
# model_2_4_endemic()
model_3_1_MSEIR()