#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Epidemiology.Models.KeelingBubonicPlague import *
import csv


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

r_r = 5
p = 0.975
k_r = 2500
d_r = 0.2
m_r = 20
g_r = 0.02
r_f = 20
k_f = 6.57
d_f = 10
beta_r = 4.7
a = 0.004

model = KeelingBubonicPlagueModel(r_r, p, k_r, d_r, m_r, g_r, r_f, k_f, d_f, beta_r, a)

model.seed_network_node_id(0, {RAT_SUSCEPTIBLE: 2500, FLEA_FREE_INFECTIOUS: 100})

model.run(10)

