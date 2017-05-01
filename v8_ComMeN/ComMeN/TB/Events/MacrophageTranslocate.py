#!/usr/bin/env python

""" A macrophage translocates to another node, along a given edge

Macrophages can move along any edge to reach another patch. Different rates for different macrophage states.
Infected macrophages also move some intracellular bacteria

"""

from ...Pulmonary.Events.PulmonaryTranslocate import *
from ..TBClasses import *
from ...Pulmonary.Node.BronchialTreeNode import *
from ...Pulmonary.Node.BronchopulmonarySegment import *
from ...Pulmonary.Node.LymphNode import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class RegularMacrophageTranslocateBronchus(TranslocateBronchus):
    """
    Macrophage moves along a bronchus. Choice is based on WEIGHT value of edge
    """
    def __init__(self, probability):
        TranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode], probability,
                                     translocate_compartment=MACROPHAGE_REGULAR,
                                     edge_choice_based_on_weight=True)


class InfectedMacrophageTranslocateBronchus(TranslocateBronchus):
    def __init__(self, probability):
        TranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode], probability,
                                     translocate_compartment=MACROPHAGE_INFECTED,
                                     internal_compartments=[BACTERIA_INTRACELLULAR],
                                     edge_choice_based_on_weight=True)


class ActivatedMacrophageTranslocateBronchus(TranslocateBronchus):
    def __init__(self, probability):
        TranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode],
                                                  probability,
                                     translocate_compartment=MACROPHAGE_ACTIVATED,
                                     edge_choice_based_on_weight=True)


class RegularMacrophageTranslocateLymph(TranslocateLymph):
    """
    Macrophage moves along a lymphatic vessel, can only move in direction of flow. Probability is based
    on FLOW RATE of edge.
    """
    def __init__(self, probability):
        TranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode], probability,
                                  translocate_compartment=MACROPHAGE_REGULAR,
                                  direction_only=True,
                                  flow_based=True)


class InfectedMacrophageTranslocateLymph(TranslocateLymph):
    def __init__(self, probability):
        TranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode], probability,
                                  translocate_compartment=MACROPHAGE_INFECTED,
                                  internal_compartments=[BACTERIA_INTRACELLULAR],
                                  direction_only=True,
                                  flow_based=True)


class ActivatedMacrophageTranslocateLymph(TranslocateLymph):
    def __init__(self, probability):
        TranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode], probability,
                                  translocate_compartment=MACROPHAGE_ACTIVATED,
                                  direction_only=True,
                                  flow_based=True)


class RegularMacrophageTranslocateBlood(TranslocateBlood):
    """
    Macrophage moves along a bloodstream edge. Can only move in direction of flow
    """
    def __init__(self, probability):
        TranslocateBlood.__init__(self, [LymphNode], probability,
                                  translocate_compartment=MACROPHAGE_REGULAR,
                                  direction_only=True)


class InfectedMacrophageTranslocateBlood(TranslocateBlood):
    def __init__(self, probability):
        TranslocateBlood.__init__(self, [LymphNode], probability,
                                  translocate_compartment=MACROPHAGE_INFECTED,
                                  internal_compartments=[BACTERIA_INTRACELLULAR],
                                  direction_only=True)


class ActivatedMacrophageTranslocateBlood(TranslocateBlood):
    def __init__(self, probability):
        TranslocateBlood.__init__(self, [LymphNode], probability,
                                  translocate_compartment=MACROPHAGE_ACTIVATED,
                                  direction_only=True)
