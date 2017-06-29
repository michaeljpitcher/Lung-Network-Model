#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Epidemiology.Arino.ArinoOneSpeciesModel import *
from v8_ComMeN.ComMeN.Epidemiology.Arino.Arino2PatchSIS import *
from v8_ComMeN.ComMeN.Epidemiology.BaseEpidemic.Graphing.PopulationGraph import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def model_Arino_one_species():

    m = 0
    betas = {0:0.5076, 1:0.4761}

    d_years = 77
    d_days = 28105
    d = 1.0/d_days
    epsilon = 1.0/4.0
    gamma = 1.0/2.0

    model = ArinoOneSpeciesModel(2, d, betas, m, epsilon, gamma)

    pop_0 = 200000
    inf_0 = 500
    pop_1 = 200000
    inf_1 = 0

    model.seed_network_node_id(0, {SUSCEPTIBLE: pop_0 - inf_0, INFECTIOUS: inf_0})
    model.seed_network_node_id(1, {SUSCEPTIBLE: pop_1 - inf_1, INFECTIOUS: inf_1})

    run_id = 1
    model.run(time_limit=800, run_id=run_id)
    draw_multi_population_graph(run_id, [INFECTIOUS], title="ARINO")


def model_Arino_2_Patch_SIS():

    b_values = (6.0, 8.0)
    beta_values = (0.235, 0.02)
    d_values = (1.0/(365*60), 1.0/(365*60))
    gamma_values = (1.0/5, 1.0/6)
    m_values = (0.045, 0.030)
    alpha_values = (0.6, 0.3)

    model = Arino2PatchSISModel(b_values, beta_values, d_values, gamma_values, m_values, alpha_values)

    pop_0 = 120000
    inf_0 = 2000
    pop_1 = 130000
    inf_1 = 4000

    model.seed_network_node_id(1, {SUSCEPTIBLE: pop_0 - inf_0, INFECTIOUS: inf_0})
    model.seed_network_node_id(2, {SUSCEPTIBLE: pop_1 - inf_1, INFECTIOUS: inf_1})

    run_id = 1
    import cProfile
    cp = cProfile.Profile()
    # cp.enable()
    model.run(time_limit=1600, run_id=run_id)
    # cp.disable()
    # cp.print_stats("cumtime")
    draw_multi_population_graph(run_id, [INFECTIOUS], title="ARINO")

# model_Arino_one_species()
model_Arino_2_Patch_SIS()

# draw_multi_population_graph(1, [INFECTIOUS], title="ARINO")