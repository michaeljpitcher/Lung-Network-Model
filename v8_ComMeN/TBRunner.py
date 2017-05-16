#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.TBIndividual.Models.TB_Model_Full import *
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

dcs_per_bps = config.getint('InitialSeedingDendriticCells', 'dcs_per_bronchopulmonarysegment')
dcs_per_btn = config.getint('InitialSeedingDendriticCells', 'dcs_per_bronchialtreenode')
dcs_per_lymph = config.getint('InitialSeedingDendriticCells', 'dcs_per_lymphnode')

# TODO - base on ventilation?
initial_fast_bacteria = dict()
for (node_id, count) in config.items('InitialSeedingBacteriaFast'):
    initial_fast_bacteria[int(node_id)] = int(count)
initial_slow_bacteria = dict()
for (node_id, count) in config.items('InitialSeedingBacteriaSlow'):
    initial_slow_bacteria[int(node_id)] = int(count)

model = TBModelFull(initial_macrophages_bps=macs_per_bps, initial_macrophages_btn=macs_per_btn,
                    initial_macrophages_lymph=macs_per_lymph,
                    initial_bacteria_fast=initial_fast_bacteria, initial_bacteria_slow=initial_slow_bacteria,
                    initial_dcs_bps=dcs_per_bps, initial_dcs_btn=dcs_per_btn, initial_dcs_lymph=dcs_per_lymph,
                    probabilities=probabilities, include_bronchials=include_bronchials,
                    tree_weight_method=tree_weight_method, include_lymphatics=include_lymphatics,
                    include_bloodstream=include_bloodstream)


# import cProfile
# cp = cProfile.Profile()
# cp.enable()
model.run(time_limit=1.0, run_id=99, debug='Debug')
# cp.disable()
# cp.print_stats('tottime')
