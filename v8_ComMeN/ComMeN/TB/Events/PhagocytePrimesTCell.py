#!/usr/bin/env python

""" Naive lymphocytes activate through contact with phagocytes

A naive lymphocyte (t-cell helper or t-cell cytotoxic) comes into contact with a phagocyte, which presents
its antigens and triggers priming of the naive cell, turning it into an effector t-cell

"""

from ...Base.Events.Change import ChangeByOtherCompartments
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

# TODO - split into 2 functions (Dend and mac) as clarification needed RE which phagocyte activates which lymphocyte


class TCellHelperActivationDendriticMature(ChangeByOtherCompartments):
    def __init__(self, probability):
        ChangeByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                           compartment_from=T_CELL_NAIVE_HELPER,
                                           compartment_to=T_CELL_HELPER,
                                           influencing_compartments=[DENDRITIC_CELL_MATURE])


class TCellHelperActivationMacrophageInfected(ChangeByOtherCompartments):
    def __init__(self, probability):
        ChangeByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                           compartment_from=T_CELL_NAIVE_HELPER,
                                           compartment_to=T_CELL_HELPER,
                                           influencing_compartments=[MACROPHAGE_INFECTED])


class TCellCytotoxicActivationDendriticMature(ChangeByOtherCompartments):
    def __init__(self, probability):
        ChangeByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                           compartment_from=T_CELL_NAIVE_CYTOTOXIC,
                                           compartment_to=T_CELL_CYTOTOXIC,
                                           influencing_compartments=[DENDRITIC_CELL_MATURE])


class TCellCytotoxicActivationMacrophageInfected(ChangeByOtherCompartments):
    def __init__(self, probability):
        ChangeByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                           compartment_from=T_CELL_NAIVE_CYTOTOXIC,
                                           compartment_to=T_CELL_CYTOTOXIC,
                                           influencing_compartments=[MACROPHAGE_INFECTED])