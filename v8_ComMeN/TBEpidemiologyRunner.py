#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Epidemiology.TB.BasicTBModel import *
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
    draw_population_graph(run_id, model.compartments, "TB Basic epdidemiology")

basic_tb_epidemic()
# model_2_4_endemic()