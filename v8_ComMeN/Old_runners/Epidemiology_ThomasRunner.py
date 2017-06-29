#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import csv

import matplotlib.pyplot as plt

from v8_ComMeN.ComMeN.Epidemiology.Thomas.ThomasSimpleModel import *
from v8_ComMeN.ComMeN.Epidemiology.BaseEpidemic.Graphing.PopulationGraph import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def model_thomas_simple():
    b = 0.0317
    mu_n = 0.0317
    mu_nt = 0.1

    c_ni = 0.09
    c_nn = 0.09
    beta_n = 5.7
    nu_n = 0.001
    epsilon_n = 0.05
    p_n = 0.7

    pop = 200000
    inf = 0.01

    model = SimpleThomasModel(b, c_nn, c_ni, beta_n, epsilon_n, p_n, mu_n, mu_nt, nu_n)
    model.seed_network_node_id(0, {SUSCEPTIBLE:pop*(1-inf), INFECTIOUS:pop*inf})
    run_id = 1
    model.run(time_limit=50, run_id=run_id)
    draw_single_population_graph(run_id, model.compartments, title="THOMAS SIMPLE")


model_thomas_simple()
