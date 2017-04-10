#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..Data import *
from ..PulmonaryClasses import *
from ..Node.BronchialTreeNode import *
from ..Node.LymphNode import *
from ...Base.Network.MetapopulationNetwork import *
from ...Base.Network.WeightFunctions import *


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class PulmonaryAnatomyNetwork(MetapopulationNetwork):

    def __init__(self, compartments, events_and_node_types, bronchial_tree_nodes=True,
                 bronchial_tree_weight_method=HORSFIELD, lymphatic_nodes=True, haematogenous_reseeding=True):

        nodes = []
        edges = []

        if bronchial_tree_nodes:
            for id in Data_BronchialTree.BRONCHIAL_TREE_IDS:
                position = Data_BronchialTree.BRONCHIAL_TREE_POSITIONS[id]
                ventilation = Data_BronchialTree.ventilation_from_position(position)
                perfusion = Data_BronchialTree.perfusion_from_position(position)
                node = BronchialTreeNode(id, compartments, ventilation, perfusion, position)
                nodes.append(node)

            edge_weights = tree_weight_calculations(0, Data_BronchialTree.BRONCHIAL_TREE_EDGES,
                                                    bronchial_tree_weight_method)

            for (u,v) in Data_BronchialTree.BRONCHIAL_TREE_EDGES:
                if (u,v) in edge_weights:
                    weight = edge_weights[(u, v)]
                else:
                    weight = edge_weights[(v, u)]
                edge_data = {EDGE_TYPE: BRONCHUS, WEIGHT: weight}
                edge = (nodes[u], nodes[v], edge_data)
                edges.append(edge)

        if lymphatic_nodes:
            for id in Data_Lymphatic.LYMPH_NODE_IDS:
                position = Data_Lymphatic.LYMPH_NODE_POSITIONS[id]
                node = LymphNode(id, compartments, position)
                nodes.append(node)

            for (u,v) in Data_Lymphatic.LYMPH_EDGES:
                edge_data = {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: v}
                edge = (nodes[u], nodes[v], edge_data)
                edges.append(edge)

        if haematogenous_reseeding:
            # TODO - blood stuff
            pass

        MetapopulationNetwork.__init__(self, compartments, nodes, edges, events_and_node_types)

