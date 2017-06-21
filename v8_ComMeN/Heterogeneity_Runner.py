#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Heterogeneity.Model.Model1 import *
from v8_ComMeN.ComMeN.Heterogeneity.Model.Model2 import *


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

def run_model_1():

    nodes = 10
    tau = 0.1
    k = 100

    model = HeterogeneityModel1(nodes, tau, k)
    model.seed_network_node_id(np.random.randint(0, nodes),{BACTERIA: 10})

    model.run(0, 100, "run1", record_steps=1)

    for n in model.nodes():
        print n.node_id, n.growth_rate, n.death_rate

def run_model_2():

    safe_nodes = 10
    dangerous_nodes = 10
    tau = 0.1
    k = 100

    model = HeterogeneityModel2(safe_nodes, dangerous_nodes, tau, k)
    model.seed_network_node_id(np.random.randint(0, safe_nodes+dangerous_nodes),{BACTERIA: 10})

    model.run(0, 100, "run1", record_steps=1)

    for n in model.nodes():
        print n.node_id, n.growth_rate, n.death_rate


run_model_2()