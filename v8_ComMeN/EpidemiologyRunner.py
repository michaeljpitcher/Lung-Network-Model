#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Epidemiology.Models.DetailedBlowerModel import *
import csv


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

population_size = 200000
infection_size = 1
pi = 4400
p = 0.05
beta = 0.00005
f = 0.7
mu = 0.0222
v = 0.00256
q = 0.85
mu_t = 0.139
c = 0.058
omega = 0.005

model = DetailedBlowerModel(population_size, infection_size, pi=pi, p=p, beta=beta, f=f, mu=mu, v=v, q=q, mu_t=mu_t,
                            c=c, omega=omega)

model.run(100)


with open('fast.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for key in range(0, int(max(model.fast_incidence_rate.keys()))):
        if float(key) in model.fast_incidence_rate.keys():
            csvwriter.writerow([key, model.fast_incidence_rate[float(key)]])
        else:
            csvwriter.writerow([key, 0])

with open('slow.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for key in range(0, int(max(model.slow_incidence_rate.keys()))):
        if float(key) in model.slow_incidence_rate.keys():
            csvwriter.writerow([key, model.slow_incidence_rate[float(key)]])
        else:
            csvwriter.writerow([key, 0])

with open('relapse.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for key in range(0, int(max(model.relapse_incidence_rate.keys()))):
        if float(key) in model.relapse_incidence_rate.keys():
            csvwriter.writerow([key, model.relapse_incidence_rate[float(key)]])
        else:
            csvwriter.writerow([key, 0])