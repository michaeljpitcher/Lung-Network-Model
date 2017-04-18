#!/usr/bin/env python

"""Short docstring

Long Docstring

"""


from ..Data.Data_BronchialTree import *
from ..Data.Data_Lymphatic import *
from ..Data.Data_HaematogenousReseed import *
from ..PulmonaryClasses import *
from ..Node.BronchialTreeNode import *
from ..Node.BronchopulmonarySegment import *
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

    def __init__(self, compartments, events, bronchial_tree_nodes=True,
                 bronchial_tree_weight_method=HORSFIELD, lymphatic_nodes=True, haematogenous_reseeding=True):

        nodes = []
        edges = []

        if bronchial_tree_nodes:
            for id in BRONCHIAL_TREE_NODE_IDS:
                position = BRONCHIAL_TREE_NODE_POSITIONS[id]
                ventilation = ventilation_from_position(position)
                perfusion = perfusion_from_position(position)
                node = BronchialTreeNode(id, compartments, ventilation, perfusion, position)
                nodes.append(node)
                
            for id in BRONCHOPULMONARY_SEGMENT_IDS:
                position = BRONCHOPULMONARY_SEGMENT_POSITIONS[id]
                ventilation = ventilation_from_position(position)
                perfusion = perfusion_from_position(position)
                node = BronchopulmonarySegment(id, compartments, ventilation, perfusion, position)
                nodes.append(node)

            edge_weights = tree_weight_calculations(0, BRONCHIAL_TREE_EDGES, bronchial_tree_weight_method)

            for (u,v) in BRONCHIAL_TREE_EDGES:
                if (u,v) in edge_weights:
                    weight = edge_weights[(u, v)]
                else:
                    weight = edge_weights[(v, u)]
                edge_data = {EDGE_TYPE: BRONCHUS, WEIGHT: weight}
                edge = (nodes[u], nodes[v], edge_data)
                edges.append(edge)

        if lymphatic_nodes:
            for id in LYMPH_NODE_IDS:
                position = LYMPH_NODE_POSITIONS[id]
                node = LymphNode(id, compartments, position)
                nodes.append(node)

            flow_rates = calculate_lymph_flow_rates(BRONCHOPULMONARY_SEGMENT_POSITIONS)

            for (u,v) in LYMPH_EDGES:
                edge_data = {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: nodes[v], FLOW_RATE: flow_rates[(u,v)]}
                edge = (nodes[u], nodes[v], edge_data)
                edges.append(edge)

        if haematogenous_reseeding:
            for (u, v) in HAEMATOGENOUS_EDGES:
                edge_data = {EDGE_TYPE: HAEMATOGENOUS, DIRECTION: nodes[v]}
                edge = (nodes[u], nodes[v], edge_data)
                edges.append(edge)

        MetapopulationNetwork.__init__(self, compartments, nodes, edges, events)
