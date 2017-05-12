#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Epidemiology.TB.BasicTBModel import *
from v8_ComMeN.ComMeN.Epidemiology.TB.TBModel2 import *
from v8_ComMeN.ComMeN.Epidemiology.BaseEpidemic.Graphing.PopulationGraph import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def basic_tb_epidemic():
    beta = 40
    gamma = 0.001
    delta = 0.1
    omega = 0.1

    model = BasicTBEpidemicModel(beta, gamma, delta, omega)
    model.seed_network_node_id(0, {SUSCEPTIBLE:990, INFECTIOUS:10})
    run_id = 1
    model.run(100, run_id=run_id)
    draw_population_graph(run_id, model.compartments, "TB Basic epidemiology")


def run_tb_model_2():
    beta = 4 # Infection rate
    gamma = 0.001 # Progression
    p = 0.1 # Prob of becoming infectious over latent
    delta = 0.1 # Recovery rate
    omega = 0.1 # Birth/death rate
    omega_i = 0.01 # Death due to infection

    model = TBEpidemicModel2(beta=beta, gamma=gamma, p=p, delta=delta, omega=omega, omega_i=omega_i)
    model.seed_network_node_id(0, {SUSCEPTIBLE:990, INFECTIOUS:10})
    run_id = 1
    model.run(200, run_id=run_id)
    draw_population_graph(run_id, model.compartments, "TB Basic epidemiology")


# basic_tb_epidemic()
run_tb_model_2()