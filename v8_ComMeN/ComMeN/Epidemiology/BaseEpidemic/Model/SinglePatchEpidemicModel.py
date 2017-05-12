#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Base.Network.MetapopulationNetwork import *
from v8_ComMeN.ComMeN.Base.Node.Patch import *


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class SinglePatchEpidemicModel(MetapopulationNetwork):

    def __init__(self, compartments, events):
        node = Patch(0, compartments)
        MetapopulationNetwork.__init__(self, compartments, [node], [], events)

    def seed_network(self, seeding):
        MetapopulationNetwork.seed_network_node_id(self, 0, seeding)
