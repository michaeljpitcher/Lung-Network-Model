#!/usr/bin/env python

""" Macrophage phagocytoses a bacterium

Macrophage ingests a bacteria. Mtb often prevents the intended destruction by the macrophage and remains alive as an
intracellular bacterium. Macrophages with intracellular bacteria change to infected state which drives other activity 
(death, reduced movement, etc). Activated macrophages always destroy their bacteria.

Macrophages with intracellular bacteria can destroy them; if they clear all of them, they become regular.

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

# TODO - may need something here for chemokine - i.e. chemokine increases macrophage movement, thus increasing ingestion rates


class RegularMacrophageIngestFastBacteriaRetain(Phagocytosis):
    """
    Macrophage ingests a Fast bacterium but cannot destroy it. Bacterium turns intracellular, macrophage turns infected
    """
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_REGULAR,
                              compartment_to_ingest=BACTERIA_FAST,
                              compartment_to_change_phagocyte_to=MACROPHAGE_INFECTED,
                              compartment_to_change_ingested_to=BACTERIA_INTRACELLULAR)


class RegularMacrophageIngestFastBacteriaDestroy(Phagocytosis):
    """
    Macrophage ingests a Fast bacterium and destroys it. Bacterium disappears, macrophage remains the same
    """
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
    """
    Infected macrophage ingests a Fast bacterium but cannot destroy it. Bacterium turns intracellular
    """
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=MACROPHAGE_INFECTED,
                              compartment_to_ingest=BACTERIA_FAST,
                              compartment_to_change_ingested_to=BACTERIA_INTRACELLULAR)


class InfectedMacrophageIngestFastBacteriaDestroy(Phagocytosis):
    """
    Infected macrophage ingests a Fast bacterium and destroys it. Bacterium disappears
    """
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
    """
    Activated macrophage ingests a Fast bacterium and destroys it. Bacterium disappears
    """
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
    """
    Infected macrophage destroys an internal bacterium. Bacterium disappears. If all bacteria cleared, macrophage turns
    back to regular
    """
    def __init__(self, probability):
        PhagocyteDestroyInternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                           probability,
                                           phagocyte_compartment=MACROPHAGE_INFECTED,
                                           internal_compartment=BACTERIA_INTRACELLULAR,
                                           healed_phagocyte_compartment=MACROPHAGE_REGULAR)
