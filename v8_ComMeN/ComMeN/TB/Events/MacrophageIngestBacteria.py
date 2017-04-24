#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Pulmonary.Events.PhagocyteIngestBacteria import *
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


class RegularMacrophageIngestFastBacteriaRetain(PhagocyteIngestBacteria):
    def __init__(self, probability):
        PhagocyteIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                         phagocyte_compartment=MACROPHAGE_REGULAR,
                                         bacteria_compartment=BACTERIA_FAST,
                                         phagocyte_change_compartment=MACROPHAGE_INFECTED,
                                         bacteria_change_compartment=BACTERIA_INTRACELLULAR)


class RegularMacrophageIngestFastBacteriaDestroy(PhagocyteIngestBacteria):
    def __init__(self, probability):
        PhagocyteIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                         phagocyte_compartment=MACROPHAGE_REGULAR,
                                         bacteria_compartment=BACTERIA_FAST)


class RegularMacrophageIngestSlowBacteriaRetain(PhagocyteIngestBacteria):
    def __init__(self, probability):
        PhagocyteIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                         phagocyte_compartment=MACROPHAGE_REGULAR,
                                         bacteria_compartment=BACTERIA_SLOW,
                                         phagocyte_change_compartment=MACROPHAGE_INFECTED,
                                         bacteria_change_compartment=BACTERIA_INTRACELLULAR)


class RegularMacrophageIngestSlowBacteriaDestroy(PhagocyteIngestBacteria):
    def __init__(self, probability):
        PhagocyteIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                         phagocyte_compartment=MACROPHAGE_REGULAR,
                                         bacteria_compartment=BACTERIA_SLOW)


class InfectedMacrophageIngestFastBacteriaRetain(PhagocyteIngestBacteria):
    def __init__(self, probability):
        PhagocyteIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                         phagocyte_compartment=MACROPHAGE_INFECTED,
                                         bacteria_compartment=BACTERIA_FAST,
                                         bacteria_change_compartment=BACTERIA_INTRACELLULAR)


class InfectedMacrophageIngestFastBacteriaDestroy(PhagocyteIngestBacteria):
    def __init__(self, probability):
        PhagocyteIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                         phagocyte_compartment=MACROPHAGE_INFECTED,
                                         bacteria_compartment=BACTERIA_FAST)


class InfectedMacrophageIngestSlowBacteriaRetain(PhagocyteIngestBacteria):
    def __init__(self, probability):
        PhagocyteIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                         phagocyte_compartment=MACROPHAGE_INFECTED,
                                         bacteria_compartment=BACTERIA_SLOW,
                                         bacteria_change_compartment=BACTERIA_INTRACELLULAR)


class InfectedMacrophageIngestSlowBacteriaDestroy(PhagocyteIngestBacteria):
    def __init__(self, probability):
        PhagocyteIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                         phagocyte_compartment=MACROPHAGE_INFECTED,
                                         bacteria_compartment=BACTERIA_SLOW)


class ActivatedMacrophageIngestFastBacteriaDestroy(PhagocyteIngestBacteria):
    def __init__(self, probability):
        PhagocyteIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                         phagocyte_compartment=MACROPHAGE_ACTIVATED,
                                         bacteria_compartment=BACTERIA_FAST)


class ActivatedMacrophageIngestSlowBacteriaDestroy(PhagocyteIngestBacteria):
    def __init__(self, probability):
        PhagocyteIngestBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                         phagocyte_compartment=MACROPHAGE_ACTIVATED,
                                         bacteria_compartment=BACTERIA_SLOW)


class InfectedMacrophageDestroyInternalBacteria(PhagocyteDestroyInternalBacteria):
    def __init__(self, probability):
        PhagocyteDestroyInternalBacteria.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                  probability,
                                                  phagocyte_compartment=MACROPHAGE_INFECTED,
                                                  bacteria_compartment=BACTERIA_INTRACELLULAR,
                                                  healed_phagocyte_compartment=MACROPHAGE_REGULAR)
