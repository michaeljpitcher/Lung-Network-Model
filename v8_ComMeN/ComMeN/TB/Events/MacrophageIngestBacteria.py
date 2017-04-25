#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Phagocytosis import *
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


class RegularMacrophageIngestFastBacteriaRetain(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_REGULAR,
                              compartment_to_ingest=BACTERIA_FAST,
                              compartment_to_change_phagocyte_to=MACROPHAGE_INFECTED,
                              compartment_to_change_ingested_to=BACTERIA_INTRACELLULAR)


class RegularMacrophageIngestFastBacteriaDestroy(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_REGULAR,
                              compartment_to_ingest=BACTERIA_FAST)


class RegularMacrophageIngestSlowBacteriaRetain(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_REGULAR,
                              compartment_to_ingest=BACTERIA_SLOW,
                              compartment_to_change_phagocyte_to=MACROPHAGE_INFECTED,
                              compartment_to_change_ingested_to=BACTERIA_INTRACELLULAR)


class RegularMacrophageIngestSlowBacteriaDestroy(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_REGULAR,
                              compartment_to_ingest=BACTERIA_SLOW)


class InfectedMacrophageIngestFastBacteriaRetain(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_INFECTED,
                              compartment_to_ingest=BACTERIA_FAST,
                              compartment_to_change_ingested_to=BACTERIA_INTRACELLULAR)


class InfectedMacrophageIngestFastBacteriaDestroy(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_INFECTED,
                              compartment_to_ingest=BACTERIA_FAST)


class InfectedMacrophageIngestSlowBacteriaRetain(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_INFECTED,
                              compartment_to_ingest=BACTERIA_SLOW,
                              compartment_to_change_ingested_to=BACTERIA_INTRACELLULAR)


class InfectedMacrophageIngestSlowBacteriaDestroy(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_INFECTED,
                              compartment_to_ingest=BACTERIA_SLOW)


class ActivatedMacrophageIngestFastBacteriaDestroy(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_ACTIVATED,
                              compartment_to_ingest=BACTERIA_FAST)


class ActivatedMacrophageIngestSlowBacteriaDestroy(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_ACTIVATED,
                              compartment_to_ingest=BACTERIA_SLOW)


class InfectedMacrophageDestroyInternalBacteria(PhagocyteDestroyInternals):
    def __init__(self, probability):
        PhagocyteDestroyInternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                           probability,
                                           phagocyte_compartment=MACROPHAGE_INFECTED,
                                           internal_compartment=BACTERIA_INTRACELLULAR,
                                           healed_phagocyte_compartment=MACROPHAGE_REGULAR)
