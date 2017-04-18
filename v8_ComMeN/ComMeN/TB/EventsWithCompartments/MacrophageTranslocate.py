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
                                               probability, MACROPHAGE_REGULAR, True)


class InfectedMacrophageTranslocateBronchus(MacrophageTranslocateBronchus):
    def __init__(self, probability):
        MacrophageTranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode],
                                               probability, MACROPHAGE_INFECTED, True, BACTERIA_INTRACELLULAR)


class ActivatedMacrophageTranslocateBronchus(MacrophageTranslocateBronchus):
    def __init__(self, probability):
        MacrophageTranslocateBronchus.__init__(self, [BronchopulmonarySegment, BronchialTreeNode],
                                               probability, MACROPHAGE_ACTIVATED, True)


class RegularMacrophageTranslocateLymph(MacrophageTranslocateLymph):
    def __init__(self, probability):
        MacrophageTranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode], probability, MACROPHAGE_REGULAR,
                                            True)


class InfectedMacrophageTranslocateLymph(MacrophageTranslocateLymph):
    def __init__(self, probability):
        MacrophageTranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode],
                                            probability, MACROPHAGE_INFECTED, True, BACTERIA_INTRACELLULAR)


class ActivatedMacrophageTranslocateLymph(MacrophageTranslocateLymph):
    def __init__(self, probability):
        MacrophageTranslocateLymph.__init__(self, [BronchopulmonarySegment, LymphNode],
                                            probability, MACROPHAGE_ACTIVATED, True)


class RegularMacrophageTranslocateBlood(MacrophageTranslocateBlood):
    def __init__(self, probability):
        MacrophageTranslocateBlood.__init__(self, [LymphNode], probability, MACROPHAGE_REGULAR, True)


class InfectedMacrophageTranslocateBlood(MacrophageTranslocateBlood):
    def __init__(self, probability):
        MacrophageTranslocateBlood.__init__(self, [LymphNode], probability, MACROPHAGE_INFECTED, True,
                                            BACTERIA_INTRACELLULAR)


class ActivatedMacrophageTranslocateBlood(MacrophageTranslocateBlood):
    def __init__(self, probability):
        MacrophageTranslocateBlood.__init__(self, [LymphNode], probability, MACROPHAGE_ACTIVATED, True)
