#!/usr/bin/env python

"""Short docstring

Long Docstring

"""


from ..Events.MacrophageTranslocate import *
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


class RegularMacrophageTranslocateBronchus(MacrophageTranslocateBronchus):
    def __init__(self, probability):
        MacrophageTranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode],
                                               probability,
                                               macrophage_compartment=MACROPHAGE_REGULAR,
                                               edge_choice_based_on_weight=True)


class InfectedMacrophageTranslocateBronchus(MacrophageTranslocateBronchus):
    def __init__(self, probability):
        MacrophageTranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode],
                                               probability, macrophage_compartment=MACROPHAGE_INFECTED,
                                               edge_choice_based_on_weight=True,
                                               bacteria_compartment_to_translocate=BACTERIA_INTRACELLULAR)


class ActivatedMacrophageTranslocateBronchus(MacrophageTranslocateBronchus):
    def __init__(self, probability):
        MacrophageTranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode],
                                               probability,
                                               macrophage_compartment=MACROPHAGE_ACTIVATED,
                                               edge_choice_based_on_weight=True)


class RegularMacrophageTranslocateLymph(MacrophageTranslocateLymph):
    def __init__(self, probability):
        MacrophageTranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode], probability,
                                            macrophage_compartment=MACROPHAGE_REGULAR,
                                            direction_only=True)


class InfectedMacrophageTranslocateLymph(MacrophageTranslocateLymph):
    def __init__(self, probability):
        MacrophageTranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode],
                                            probability, macrophage_compartment=MACROPHAGE_INFECTED,
                                            direction_only=True,
                                            bacteria_compartment_to_translocate=BACTERIA_INTRACELLULAR)


class ActivatedMacrophageTranslocateLymph(MacrophageTranslocateLymph):
    def __init__(self, probability):
        MacrophageTranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode],
                                            probability, macrophage_compartment=MACROPHAGE_ACTIVATED,
                                            direction_only=True)


class RegularMacrophageTranslocateBlood(MacrophageTranslocateBlood):
    def __init__(self, probability):
        MacrophageTranslocateBlood.__init__(self, [LymphNode], probability, macrophage_compartment=MACROPHAGE_REGULAR,
                                            direction_only=True)


class InfectedMacrophageTranslocateBlood(MacrophageTranslocateBlood):
    def __init__(self, probability):
        MacrophageTranslocateBlood.__init__(self, [LymphNode], probability, macrophage_compartment=MACROPHAGE_INFECTED,
                                            direction_only=True,
                                            bacteria_compartment_to_translocate=BACTERIA_INTRACELLULAR)


class ActivatedMacrophageTranslocateBlood(MacrophageTranslocateBlood):
    def __init__(self, probability):
        MacrophageTranslocateBlood.__init__(self, [LymphNode], probability, macrophage_compartment=MACROPHAGE_ACTIVATED,
                                            direction_only=True)
