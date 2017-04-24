#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..Events.MacrophageIngestBacteria import *
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


class RegularMacrophageIngestFastBacteriaRetain(MacrophageIngestBacteria):
    def __init__(self, probability):
        MacrophageIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                          macrophage_compartment=MACROPHAGE_REGULAR,
                                          bacteria_compartment=BACTERIA_FAST,
                                          macrophage_change_compartment=MACROPHAGE_INFECTED,
                                          bacteria_change_compartment=BACTERIA_INTRACELLULAR)


class RegularMacrophageIngestFastBacteriaDestroy(MacrophageIngestBacteria):
    def __init__(self, probability):
        MacrophageIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                          macrophage_compartment=MACROPHAGE_REGULAR,
                                          bacteria_compartment=BACTERIA_FAST)


class RegularMacrophageIngestSlowBacteriaRetain(MacrophageIngestBacteria):
    def __init__(self, probability):
        MacrophageIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                          macrophage_compartment=MACROPHAGE_REGULAR,
                                          bacteria_compartment=BACTERIA_SLOW,
                                          macrophage_change_compartment=MACROPHAGE_INFECTED,
                                          bacteria_change_compartment=BACTERIA_INTRACELLULAR)


class RegularMacrophageIngestSlowBacteriaDestroy(MacrophageIngestBacteria):
    def __init__(self, probability):
        MacrophageIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                          macrophage_compartment=MACROPHAGE_REGULAR,
                                          bacteria_compartment=BACTERIA_SLOW)


class InfectedMacrophageIngestFastBacteriaRetain(MacrophageIngestBacteria):
    def __init__(self, probability):
        MacrophageIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                          macrophage_compartment=MACROPHAGE_INFECTED,
                                          bacteria_compartment=BACTERIA_FAST,
                                          bacteria_change_compartment=BACTERIA_INTRACELLULAR)


class InfectedMacrophageIngestFastBacteriaDestroy(MacrophageIngestBacteria):
    def __init__(self, probability):
        MacrophageIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                          macrophage_compartment=MACROPHAGE_INFECTED,
                                          bacteria_compartment=BACTERIA_FAST)


class InfectedMacrophageIngestSlowBacteriaRetain(MacrophageIngestBacteria):
    def __init__(self, probability):
        MacrophageIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                          macrophage_compartment=MACROPHAGE_INFECTED,
                                          bacteria_compartment=BACTERIA_SLOW,
                                          bacteria_change_compartment=BACTERIA_INTRACELLULAR)


class InfectedMacrophageIngestSlowBacteriaDestroy(MacrophageIngestBacteria):
    def __init__(self, probability):
        MacrophageIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                          macrophage_compartment=MACROPHAGE_INFECTED,
                                          bacteria_compartment=BACTERIA_SLOW)


class ActivatedMacrophageIngestFastBacteriaDestroy(MacrophageIngestBacteria):
    def __init__(self, probability):
        MacrophageIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                          macrophage_compartment=MACROPHAGE_ACTIVATED,
                                          bacteria_compartment=BACTERIA_FAST)


class ActivatedMacrophageIngestSlowBacteriaDestroy(MacrophageIngestBacteria):
    def __init__(self, probability):
        MacrophageIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                          macrophage_compartment=MACROPHAGE_ACTIVATED,
                                          bacteria_compartment=BACTERIA_SLOW)


class InfectedMacrophageDestroyInternalBacteria(MacrophageDestroyInternalBacteria):
    def __init__(self, probability):
        MacrophageDestroyInternalBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                   probability,
                                                   macrophage_compartment=MACROPHAGE_INFECTED,
                                                   bacteria_compartment=BACTERIA_INTRACELLULAR,
                                                   healed_macrophage_compartment=MACROPHAGE_REGULAR)
