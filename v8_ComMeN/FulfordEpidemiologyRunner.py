#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Epidemiology.Models.FulfordMetapopulationModelSingle import *
import csv


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

# Birth and death rates are same everywhere
B = 0
D_1 = 0
D_2 = 0

patch_data = {0: {BIRTH_RATE: B, DEATH_RATE_JUVENILE: D_1, DEATH_RATE_MATURE: D_2, AREA:0}}

beta_nu = 0
sigma = 0
alpha = 0
a = 0
z = 0
s = 0
beta_11 = beta_12 = beta_21 = beta_22 = 0
c_11 = c_12 = c_21 = c_22 = 0

#
model = FulfordMetapopultionModel(patch_data, {}, beta_nu, sigma, alpha, a, z, s, beta_11, beta_12, beta_21, beta_22, c_11,
                 c_12, c_21, c_22)

model.run(10)
