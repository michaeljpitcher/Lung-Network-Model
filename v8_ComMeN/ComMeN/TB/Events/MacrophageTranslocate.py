#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Pulmonary.Events.PhagocyteTranslocate import *
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


class RegularMacrophageTranslocateBronchus(PhagocyteTranslocateBronchus):
    def __init__(self, probability):
        PhagocyteTranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode],
                                              probability,
                                              phagocyte_compartment=MACROPHAGE_REGULAR,
                                              edge_choice_based_on_weight=True)


class InfectedMacrophageTranslocateBronchus(PhagocyteTranslocateBronchus):
    def __init__(self, probability):
        PhagocyteTranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode],
                                              probability, phagocyte_compartment=MACROPHAGE_INFECTED,
                                              edge_choice_based_on_weight=True,
                                              internal_compartment_to_translocate=BACTERIA_INTRACELLULAR)


class ActivatedMacrophageTranslocateBronchus(PhagocyteTranslocateBronchus):
    def __init__(self, probability):
        PhagocyteTranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode],
                                              probability,
                                              phagocyte_compartment=MACROPHAGE_ACTIVATED,
                                              edge_choice_based_on_weight=True)


class RegularMacrophageTranslocateLymph(PhagocyteTranslocateLymph):
    def __init__(self, probability):
        PhagocyteTranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode], probability,
                                           phagocyte_compartment=MACROPHAGE_REGULAR,
                                           direction_only=True)


class InfectedMacrophageTranslocateLymph(PhagocyteTranslocateLymph):
    def __init__(self, probability):
        PhagocyteTranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode],
                                           probability, phagocyte_compartment=MACROPHAGE_INFECTED,
                                           direction_only=True,
                                           internal_compartment_to_translocate=BACTERIA_INTRACELLULAR)


class ActivatedMacrophageTranslocateLymph(PhagocyteTranslocateLymph):
    def __init__(self, probability):
        PhagocyteTranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode],
                                           probability, phagocyte_compartment=MACROPHAGE_ACTIVATED,
                                           direction_only=True)


class RegularMacrophageTranslocateBlood(PhagocyteTranslocateBlood):
    def __init__(self, probability):
        PhagocyteTranslocateBlood.__init__(self, [LymphNode], probability, phagocyte_compartment=MACROPHAGE_REGULAR,
                                           direction_only=True)


class InfectedMacrophageTranslocateBlood(PhagocyteTranslocateBlood):
    def __init__(self, probability):
        PhagocyteTranslocateBlood.__init__(self, [LymphNode], probability, phagocyte_compartment=MACROPHAGE_INFECTED,
                                           direction_only=True,
                                           bacteria_compartment_to_translocate=BACTERIA_INTRACELLULAR)


class ActivatedMacrophageTranslocateBlood(PhagocyteTranslocateBlood):
    def __init__(self, probability):
        PhagocyteTranslocateBlood.__init__(self, [LymphNode], probability, phagocyte_compartment=MACROPHAGE_ACTIVATED,
                                           direction_only=True)
