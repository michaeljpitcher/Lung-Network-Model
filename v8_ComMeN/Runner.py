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
probability_sections = ["BacterialEventProbabilities", "MacrophageEventProbabilities", "TCellEventProbabilities"]
probabilities = dict()
for section in probability_sections:
    for event in config.items(section):
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

model.run(1)
