#!/usr/bin/env python

""" T-cell translocation

A t-cell moves from one node to another

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

# TODO - naive versions can't move?

class TCellHelperTranslocateBronchus(TranslocateBronchus):
    """
    Helper T-cell moves along a bronchus, choice of bronchus based on edge weights
    """
    def __init__(self, probability):
        TranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode], probability,
                                     translocate_compartment=T_CELL_HELPER,
                                     edge_choice_based_on_weight=True)


class TCellHelperTranslocateLymph(TranslocateLymph):
    """
    Helper T-cell moves along a lymphatic vessel, in direction of flow, prob of moving based on flow rate
    """
    def __init__(self, probability):
        TranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode], probability,
                                  translocate_compartment=T_CELL_HELPER,
                                  direction_only=True,
                                  flow_based=True)


class TCellHelperTranslocateBlood(TranslocateBlood):
    """
    Helper T-cell moves along a bloodstream edge, in direction of flow
    """
    def __init__(self, probability):
        TranslocateBlood.__init__(self, [LymphNode], probability,
                                  translocate_compartment=T_CELL_HELPER,
                                  direction_only=True)


class TCellCytotoxicTranslocateBronchus(TranslocateBronchus):
    def __init__(self, probability):
        TranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode], probability,
                                     translocate_compartment=T_CELL_CYTOTOXIC,
                                     edge_choice_based_on_weight=True)


class TCellCytotoxicTranslocateLymph(TranslocateLymph):
    def __init__(self, probability):
        TranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode], probability,
                                  translocate_compartment=T_CELL_CYTOTOXIC,
                                  direction_only=True,
                                  flow_based=True)


class TCellCytotoxicTranslocateBlood(TranslocateBlood):
    def __init__(self, probability):
        TranslocateBlood.__init__(self, [LymphNode], probability,
                                  translocate_compartment=T_CELL_CYTOTOXIC,
                                  direction_only=True)

