#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.TB.Models.TB_Model_Full import *
import ConfigParser as cp

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


# Load config
config_file = 'TB_model.config'
config = cp.ConfigParser()
# Force config to keep upper case
config.optionxform = str
if not config.read(config_file):
    raise IOError("Configuration file (" + config_file + ") not found")

# Read topology from config
include_bronchials = config.getboolean("TopologyParameters", "bronchial_tree")
tree_weight_method = config.get("TopologyParameters", "bronchial_tree_weight_method")
include_lymphatics = config.getboolean("TopologyParameters", "lymphatics")
include_bloodstream = config.getboolean("TopologyParameters", "bloodstream")

# Read probabilities from config
probabilities = dict()

for event in config.items('EventProbabilities'):
    assert event not in probabilities.keys(), "Event {0} has already been defined".format(event)
    probabilities[event[0]] = float(event[1])

macs_per_bps = config.getint('InitialSeedingMacrophages', 'macrophages_per_bronchopulmonarysegment')
macs_per_btn = config.getint('InitialSeedingMacrophages', 'macrophages_per_bronchialtreenode')
macs_per_lymph = config.getint('InitialSeedingMacrophages', 'macrophages_per_lymphnode')

# TODO - base on ventilation?
initial_fast_bacteria = dict()
for (node_id, count) in config.items('InitialSeedingBacteriaFast'):
    initial_fast_bacteria[int(node_id)] = int(count)
initial_slow_bacteria = dict()
for (node_id, count) in config.items('InitialSeedingBacteriaSlow'):
    initial_slow_bacteria[int(node_id)] = int(count)

model = TBModelFull(macs_per_bps, macs_per_btn, macs_per_lymph, initial_fast_bacteria, initial_slow_bacteria,
                    probabilities, include_bronchials=include_bronchials,
                     tree_weight_method=tree_weight_method, include_lymphatics=include_lymphatics,
                     include_bloodstream=include_bloodstream)

from ComMeN.Pulmonary.Visuals.PulmonaryNetworkGraph import *

"""
draw_pulmonary_network_graph(model, "ComMeN", "commen_base", False, False)
draw_pulmonary_network_graph(model, "ComMeN", "commen_lymph", True, False)
draw_pulmonary_network_graph(model, "ComMeN", "commen_all", True, True)


import cProfile
cp = cProfile.Profile()
cp.enable()
model.run(1.0, run_id=99, debug='Debug')
cp.disable()
cp.print_stats('tottime')
"""