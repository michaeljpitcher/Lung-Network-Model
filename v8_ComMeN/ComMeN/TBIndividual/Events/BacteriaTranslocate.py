#!/usr/bin/env python

"""Bacterial translocation

Bacteria can move from one patch to another along any of the edge types.

"""

from ...Pulmonary.Events.PulmonaryTranslocate import *
from ..TBClasses import *
from ...Pulmonary.Node.BronchopulmonarySegment import *
from ...Pulmonary.Node.BronchialTreeNode import *
from ...Pulmonary.Node.LymphNode import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class BacteriaTranslocateBronchusFast(TranslocateBronchus):
    """
    Fast Bacterium moves along a bronchus edge. The choice of bronchus is based on the WEIGHT value of the edge
    """
    def __init__(self, probability):
        TranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode], probability,
                                     translocate_compartment=BACTERIA_FAST,
                                     edge_choice_based_on_weight=True)


class BacteriaTranslocateBronchusSlow(TranslocateBronchus):
    def __init__(self, probability):
        TranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode], probability,
                                     translocate_compartment=BACTERIA_SLOW,
                                     edge_choice_based_on_weight=True)


class BacteriaTranslocateLymphFast(TranslocateLymph):
    """
    Fast Bacterium moves along a lymph edge. Can only move in the direction of flow. 
    More likely the higher the flow rate is.
    """
    def __init__(self, probability):
        TranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode], probability,
                                  translocate_compartment=BACTERIA_FAST,
                                  direction_only=True,
                                  flow_based=True)


class BacteriaTranslocateLymphSlow(TranslocateLymph):
    def __init__(self, probability):
        TranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode], probability,
                                  translocate_compartment=BACTERIA_SLOW,
                                  direction_only=True,
                                  flow_based=True)


class BacteriaTranslocateHaematogenousFast(TranslocateBlood):
    """
    Fast Bacterium moves along a bloodstream edge. Can only move in the direction of flow. 
    """
    def __init__(self, probability):
        TranslocateBlood.__init__(self, [LymphNode], probability,
                                  translocate_compartment=BACTERIA_FAST,
                                  direction_only=True)


class BacteriaTranslocateHaematogenousSlow(TranslocateBlood):
    def __init__(self, probability):
        TranslocateBlood.__init__(self, [LymphNode], probability,
                                  translocate_compartment=BACTERIA_SLOW,
                                  direction_only=True)
