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


class MultiPatchFullConnectedEpidemicModel(MetapopulationNetwork):

    def __init__(self, number_of_patches, compartments, events):
        nodes = []
        for n in range(number_of_patches):
            nodes.append(Patch(n, compartments))
        edges = []
        for n in range(number_of_patches-1):
            for k in range(n+1, number_of_patches):
                edges.append((nodes[n], nodes[k], {EDGE_TYPE:'edge'}))
        MetapopulationNetwork.__init__(self, compartments, nodes, edges, events)
