#!/usr/bin/env python

"""Short docstring

Long Docstring

"""


from v8_ComMeN.ComMeN.Epidemiology.Old.Lloyd.LloydModel import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def model_lloyd():
    number_of_patches = 2

    mu = 0.02
    beta = 0.0010107
    epsilon = 0.01
    sigma = 45.6
    gamma = 73.0

    model = LloydModel(number_of_patches, mu, beta, epsilon, sigma, gamma)

    pop = 10**6
    inf = 10

    model.seed_network_node_id(0, {SUSCEPTIBLE: pop - inf, INFECTIOUS: inf})
    model.seed_network_node_id(1, {SUSCEPTIBLE: pop})

    run_id = 1
    model.run(time_limit=2, run_id=run_id)

    print model.nodes()[0].subpopulations
    print model.nodes()[1].subpopulations


model_lloyd()
