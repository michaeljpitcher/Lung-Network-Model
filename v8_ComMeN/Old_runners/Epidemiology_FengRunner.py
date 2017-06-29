#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Epidemiology.TB.BasicTBModel import *
from v8_ComMeN.ComMeN.Epidemiology.TB.TBModel2 import *
from v8_ComMeN.ComMeN.Epidemiology.TB.TBModel3 import *
from v8_ComMeN.ComMeN.Epidemiology.TB.TBModel4 import *
from v8_ComMeN.ComMeN.Epidemiology.TB.TBModel5 import *
from v8_ComMeN.ComMeN.Epidemiology.TB.TBModel6 import *
from v8_ComMeN.ComMeN.Epidemiology.TB.FengTB import *

from v8_ComMeN.ComMeN.Epidemiology.BaseEpidemic.Graphing.PopulationGraph import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


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
    model.run(time_limit=100, run_id=run_id)
    draw_single_population_graph(run_id, [INFECTIOUS], title="TB Basic epidemiology")

run_feng_tb()