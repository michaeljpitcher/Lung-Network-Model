#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Epidemiology.TB.BasicTBModel import *
from v8_ComMeN.ComMeN.Epidemiology.TB.TBModel2 import *
from v8_ComMeN.ComMeN.Epidemiology.TB.TBModel3 import *
from v8_ComMeN.ComMeN.Epidemiology.TB.TBModel4 import *
from v8_ComMeN.ComMeN.Epidemiology.TB.TBModel5 import *
from v8_ComMeN.ComMeN.Epidemiology.TB.FengTB import *

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


def run_tb_model_3():
    beta = 4  # Infection rate
    gamma = 0.001  # Progression
    p = 0.1  # Prob of becoming active over latent
    q = 0.9  # Prob of becoming infectious over non-infectious
    delta = 0.1  # Recovery rate
    omega = 0.1  # Birth/death rate
    omega_i = 0.01  # Death due to infection

    model = TBEpidemicModel3(beta=beta, gamma=gamma, p=p, q=q, delta=delta, omega=omega, omega_i=omega_i)
    model.seed_network_node_id(0, {SUSCEPTIBLE:990, INFECTIOUS:10})
    run_id = 1
    model.run(200, run_id=run_id)
    draw_population_graph(run_id, model.compartments, "TB Basic epidemiology")


def run_tb_model_4():
    beta = 4  # Infection rate
    gamma = 0.001  # Progression
    p = 0.1  # Prob of becoming active over latent
    q = 0.9  # Prob of becoming infectious over non-infectious
    delta = 0.0  # Recovery rate
    omega = 0.1  # Birth/death rate
    omega_i = 0.01  # Death due to infection
    theta = 0.0  # Treatment rate

    model = TBEpidemicModel4(beta=beta, gamma=gamma, p=p, q=q, delta=delta, theta=theta, omega=omega, omega_i=omega_i)
    model.seed_network_node_id(0, {SUSCEPTIBLE:990, INFECTIOUS:10})
    run_id = 1
    model.run(200, run_id=run_id)
    draw_population_graph(run_id, model.compartments, "TB Basic epidemiology")


def run_tb_model_5():
    beta = 1  # Infection rate
    gamma = 0.001  # Progression
    p = 0.1  # Prob of becoming active over latent
    q = 1.0  # Prob of becoming infectious over non-infectious
    delta = 0.1  # Recovery rate
    omega = 0.1  # Birth/death rate
    omega_i = 0.01  # Death due to infection
    omicron = 0.1 # Non-adherence
    theta = 0.5 # Treatment

    model = TBEpidemicModel5(beta=beta, gamma=gamma, p=p, q=q, omicron=omicron, delta=delta, theta=theta, omega=omega,
                             omega_i=omega_i)
    model.seed_network_node_id(0, {SUSCEPTIBLE:990, INFECTIOUS:10})
    run_id = 1
    model.run(200, run_id=run_id)
    draw_population_graph(run_id, model.compartments, "TB Basic epidemiology")


def run_feng_tb():
    lambda_ = 417
    mu = 0.01668
    sigma = 0.9
    k = 0.005
    d = 0.1
    r = 2
    p = 0.4

    r_0 = 0.87

    c = 1
    beta = (r_0 / (k / (k + mu))) * (mu + r + d)


    model = FengTBModel(lambda_=lambda_, mu=mu, beta=beta, c=c, sigma=sigma, k=k, d=d, r=r, p=p)
    infectious = 1100
    model.seed_network_node_id(0, {SUSCEPTIBLE: 25000-infectious, INFECTIOUS: infectious})
    run_id = 1
    model.run(100, run_id=run_id)
    draw_population_graph(run_id, [INFECTIOUS], title="TB Basic epidemiology")


# basic_tb_epidemic()
# run_tb_model_2()
# run_tb_model_3()
# run_tb_model_4()
# run_tb_model_5()
run_feng_tb()