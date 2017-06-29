#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Network.MetapopulationNetwork import *
from ..Node.LungLobe import LungLobe
from ..PulmonaryVariables import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class LobularSingleLungNetwork(MetapopulationNetwork):

    def __init__(self, compartments, events):
        # Assume a right lung
        nodes = []
        # Upper
        nodes.append(LungLobe(0, compartments, (7, 8)))
        # Middle
        nodes.append(LungLobe(1, compartments, (5, 5)))
        # Lower
        nodes.append(LungLobe(2, compartments, (6, 2)))

        edges = []
        edges.append((nodes[0], nodes[1], {EDGE_TYPE: LOBULAR_EDGE}))
        edges.append((nodes[1], nodes[2], {EDGE_TYPE: LOBULAR_EDGE}))

        MetapopulationNetwork.__init__(self, compartments, nodes, edges, events)
