#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ....Base.Network.MetapopulationNetwork import *
from ....Base.Node.Patch import *
from ...EpidemiologyClasses import *


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MultiPatchFullConnectedEpidemicModel(MetapopulationNetwork):
    """
    Multiple patches - all similar and fully connected with no edge weightings
    """

    def __init__(self, number_of_patches, compartments, events):
        nodes = []
        for n in range(number_of_patches):
            nodes.append(Patch(n, compartments))
        edges = []
        for n in range(number_of_patches-1):
            for k in range(n+1, number_of_patches):
                edges.append((nodes[n], nodes[k], {EDGE_TYPE: STANDARD_EDGE}))
        MetapopulationNetwork.__init__(self, compartments, nodes, edges, events)
