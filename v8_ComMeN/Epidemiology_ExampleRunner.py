#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Epidemiology.Example.SEIExample import *
from v8_ComMeN.ComMeN.Epidemiology.BaseEpidemic.Graphing.PopulationGraph import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def example_one():
    patches = 2

    births = [0.0222, 0.0222]
    deaths = [0.0222, 0.0222]
    deaths_by_disease = [0.139, 0.139]
    p_infectious = [0.05, 0.05]
    contacts = [0.00005,0.00001]
    infects = [1,1]
    progresses = [0.00256,0.00256]
    recovers = [0.139,0.4]
    moves = [0.1,0.1]

    populations = [200000,200000]
    infecteds = [200000*0.01,0]

    run_id = 1

    model = EgModel(patches, births=births, deaths=deaths, contacts=contacts, infects=infects, progresses=progresses,
                    recovers=recovers, moves=moves, deaths_disease=deaths_by_disease, p_infectious=p_infectious)

    for n in range(patches):
        model.seed_network_node_id(n, {SUSCEPTIBLE: populations[n]-infecteds[n], INFECTIOUS: infecteds[n]})

    model.run(0, 100, run_id, record_steps=100)

    # draw_single_population_graph(run_id, model.compartments)
    # draw_multi_population_graph(run_id, ['infectious'], axis=[0,100,0,200000])
    draw_multi_population_graph(run_id, model.compartments, axis=[0,100,0,200000])


example_one()