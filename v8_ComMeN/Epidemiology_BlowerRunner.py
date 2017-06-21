#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import csv

import matplotlib.pyplot as plt

from v8_ComMeN.ComMeN.Epidemiology.Blower.BlowerSimpleModel import *
from v8_ComMeN.ComMeN.Epidemiology.Blower.BlowerDetailedModel import *
from v8_ComMeN.ComMeN.Epidemiology.BaseEpidemic.Graphing.PopulationGraph import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def model_blower_simple():
    pi = 4400
    beta = 0.00005
    mu = 0.0222
    v = 0.00256
    p = 0.05
    mu_t = 0.139

    pop = 200000
    inf = 0.01

    model = SimpleBlowerModel(pi=pi, beta=beta, mu=mu,v=v, p=p, mu_t=mu_t)
    model.seed_network_node_id(0, {SUSCEPTIBLE:pop*(1-inf), INFECTIOUS:pop*inf})
    run_id = 1
    model.run(time_limit=100, run_id=run_id)
    draw_single_population_graph(run_id, model.compartments, title="BLOWER SIMPLE")


def model_blower_detailed():
    pi = 4400
    beta = 0.00005
    mu = 0.0222
    mu_t = 0.139
    p = 0.05
    v = 0.00256
    f = 0.7
    omega = 0.005
    c = 0.058
    q = 0.85

    pop = 1000000
    inf = 10000

    model = DetailedBlowerModel(pi=pi, p=p, beta=beta, f=f, mu=mu, v=v, q=q, mu_t=mu_t, c=c, omega=omega)
    model.seed_network_node_id(0, {SUSCEPTIBLE: pop, INFECTIOUS: inf})
    run_id = 1
    model.run(time_limit=200, run_id=run_id, record_steps=100)
    draw_single_population_graph(run_id, [INFECTIOUS, NON_INFECTIOUS], title="BLOWER DETAILED")
    # plot_incidence_rates({'fast':model.fast_incidence_rate, 'slow':model.slow_incidence_rate, 'relapse':model.relapse_incidence_rate})

model_blower_simple()
# model_blower_detailed()