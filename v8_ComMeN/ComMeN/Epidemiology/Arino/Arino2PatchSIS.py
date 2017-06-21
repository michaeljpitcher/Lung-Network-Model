#!/usr/bin/env python

"""Short docstring

[1] J. Arino, C. Sun, and W. Yang, "Revisiting a two-patch SIS model with infection during transport," Math. Med. Biol.,
 vol. 33, no. 1, pp. 29-55, 2015.

"""

from ...Base.Network.MetapopulationNetwork import *
from ..EpidemiologyClasses import *
from ...Base.Events.Creation import *
from ...Base.Events.Change import *
from ...Base.Events.Destruction import *
from ...Base.Events.Translocate import *
from ArinoInfect import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class ArinoPatch(Patch):
    def __init__(self, node_id, compartments, b, beta, d, gamma, m, alpha):
        self.b = b
        self.beta = beta
        self.d = d
        self.gamma = gamma
        self.m = m
        self.alpha = alpha
        Patch.__init__(self, node_id, compartments)


class ArinoBirth(Create):
    def __init__(self):
        Create.__init__(self, [ArinoPatch], 1, SUSCEPTIBLE)

    def increment_state_variable_from_node(self, node, network):
        return node.b


class ArinoDeath(Destroy):
    def __init__(self, compartment):
        Destroy.__init__(self, [ArinoPatch], 1, compartment)

    def increment_state_variable_from_node(self, node, network):
        return node.subpopulations[self.compartment_destroyed] * node.d


class ArinoRecover(Change):
    def __init__(self):
        Change.__init__(self, [ArinoPatch], 1, INFECTIOUS, SUSCEPTIBLE)

    def increment_state_variable_from_node(self, node, network):
        return node.subpopulations[self.compartment_from] * node.gamma


class ArinoMoveSusceptibleNoInfection(Translocate):
    def __init__(self):
        Translocate.__init__(self, [ArinoPatch], 1, SUSCEPTIBLE, STANDARD_EDGE)

    def increment_state_variable_from_node(self, node, network):
        N = sum(node.subpopulations.values())
        # return (1 - ((node.alpha * node.subpopulations[INFECTIOUS])/N)) * node.subpopulations[SUSCEPTIBLE] * node.m
        return node.m * node.subpopulations[SUSCEPTIBLE] * (1 - (node.alpha * node.subpopulations[INFECTIOUS])/N)

class ArinoMoveSusceptibleInfect(Translocate):
    def __init__(self):
        Translocate.__init__(self, [ArinoPatch], 1, SUSCEPTIBLE, STANDARD_EDGE)

    def increment_state_variable_from_node(self, node, network):
        N = sum(node.subpopulations.values())
        # return ((node.alpha * node.subpopulations[INFECTIOUS])/N) * node.subpopulations[SUSCEPTIBLE] * node.m
        return node.m * node.subpopulations[SUSCEPTIBLE] * ((node.alpha * node.subpopulations[INFECTIOUS]) / N)

    def move(self, node, neighbour):
        # move and change to infectious
        node.update_subpopulation(SUSCEPTIBLE, -1)
        neighbour.update_subpopulation(INFECTIOUS, 1)


class ArinoMoveInfectious(Translocate):
    def __init__(self):
        Translocate.__init__(self, [ArinoPatch], 1, INFECTIOUS, STANDARD_EDGE)

    def increment_state_variable_from_node(self, node, network):
        return node.subpopulations[self.translocate_compartment] * node.m


class Arino2PatchSISModel(MetapopulationNetwork):

    def __init__(self, b_values, beta_values, d_values, gamma_values, m_values, alpha_values):

        compartments = [SUSCEPTIBLE, INFECTIOUS]

        events = []
        # Birth
        events.append(ArinoBirth())
        # Infect
        events.append(ArinoInfect([ArinoPatch], SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS]))
        # Death
        events.append(ArinoDeath(SUSCEPTIBLE))
        events.append(ArinoDeath(INFECTIOUS))
        # Recover
        events.append(ArinoRecover())
        # Sus moves, no infection
        events.append(ArinoMoveSusceptibleNoInfection())
        # Sus moves, infection
        events.append(ArinoMoveSusceptibleInfect())
        # Inf moves
        events.append(ArinoMoveInfectious())
        nodes = []
        nodes.append(ArinoPatch(1, compartments, b_values[0], beta_values[0], d_values[0], gamma_values[0],
                                m_values[0], alpha_values[0]))
        nodes.append(ArinoPatch(2, compartments, b_values[1], beta_values[1], d_values[1], gamma_values[1],
                                m_values[1], alpha_values[1]))
        edges = [(nodes[0], nodes[1], {EDGE_TYPE:STANDARD_EDGE})]

        MetapopulationNetwork.__init__(self, compartments, nodes, edges, events)
