#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Epidemiology.Old.Mbah import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

sigma = 0.03
mu = 2.0
nu = 0.2
eta = 4.0
beta = 6.0
epsilon = 0.1

f0 = 0
f1 = 0

model = MbahSIRSModel(sigma, mu, nu, eta, beta, epsilon, f0, f1)

model.seed_network_node_id(0, {SUSCEPTIBLE: 100-15, INFECTIOUS:15, RECOVERED:0})
model.seed_network_node_id(1, {SUSCEPTIBLE: 100-5, INFECTIOUS:5, RECOVERED:0})

model.run(100, 'a')


