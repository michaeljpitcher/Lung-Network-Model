#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Visuals.MetapopulationNetworkGraph import *
from ..Node.LymphNode import *
from ..Node.BronchialTreeNode import *
from ..Node.BronchopulmonarySegment import *
from ..PulmonaryClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def draw_pulmonary_network_graph(network, title, save_name=None, include_lymphatics=True, include_blood=True):
    node_formatting = {BronchopulmonarySegment: {NODE_SIZE:500, NODE_COLOUR:'b'},
                       BronchialTreeNode: {NODE_SIZE:500, NODE_COLOUR:'cyan'}}
    if include_lymphatics:
        node_formatting[LymphNode] = {NODE_SIZE: 300, NODE_COLOUR: 'green'}

    edge_formatting = {BRONCHUS: {EDGE_COLOUR: 'b', EDGE_WIDTH: 6}}
    if include_lymphatics:
        edge_formatting[LYMPHATIC_VESSEL] = {EDGE_COLOUR: 'g', EDGE_WIDTH: 4}
    if include_blood:
        edge_formatting[HAEMATOGENOUS] = {EDGE_COLOUR: 'r', EDGE_WIDTH: 1}

    draw_network(network, title, node_formatting, edge_formatting, save_name)
