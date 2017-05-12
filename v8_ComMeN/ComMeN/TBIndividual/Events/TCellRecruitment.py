#!/usr/bin/env python

""" A t-cell is recruited

A naive t-cell is recruited into the node, either basic recruitment or increased by cytokine

"""

from ...Pulmonary.Events.PulmonaryRecruitment import *
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


class TCellNaiveHelperRecruitmentBronchialRegular(RecruitmentBronchial):
    """
    Naive helper T-cell recruited into bronchial tree
    """
    def __init__(self, probability):
        RecruitmentBronchial.__init__(self, probability,
                                      recruited_compartment=T_CELL_NAIVE_HELPER,
                                      based_on_perfusion=True)


class TCellNaiveHelperRecruitmentBronchialByCytokine(RecruitmentBronchialByExternals):
    """
    Naive helper T-cell recruited into bronchial tree based on cytokine levels
    """
    def __init__(self, probability):
        RecruitmentBronchialByExternals.__init__(self, probability,
                                                 recruited_compartment=T_CELL_NAIVE_HELPER,
                                                 external_compartments=CYTOKINE_PRODUCING_COMPARTMENTS,
                                                 based_on_perfusion=True)


class TCellNaiveHelperRecruitmentLymphRegular(RecruitmentLymph):
    """
    Naive helper T-cell recruited into lymph node
    """
    def __init__(self, probability):
        RecruitmentLymph.__init__(self, probability,
                                  recruited_compartment=T_CELL_NAIVE_HELPER)


class TCellNaiveHelperRecruitmentLymphByCytokine(RecruitmentLymphByExternals):
    """
    Naive helper T-cell recruited into lymph node based on cytokine levels
    """
    def __init__(self, probability):
        RecruitmentLymphByExternals.__init__(self, probability,
                                             recruited_compartment=T_CELL_NAIVE_HELPER,
                                             external_compartments=CYTOKINE_PRODUCING_COMPARTMENTS)


class TCellNaiveCytotoxicRecruitmentBronchialRegular(RecruitmentBronchial):
    def __init__(self, probability):
        RecruitmentBronchial.__init__(self, probability,
                                      recruited_compartment=T_CELL_NAIVE_CYTOTOXIC,
                                      based_on_perfusion=True)


class TCellNaiveCytotoxicRecruitmentBronchialByCytokine(RecruitmentBronchialByExternals):
    def __init__(self, probability):
        RecruitmentBronchialByExternals.__init__(self, probability,
                                                 recruited_compartment=T_CELL_NAIVE_CYTOTOXIC,
                                                 external_compartments=CYTOKINE_PRODUCING_COMPARTMENTS,
                                                 based_on_perfusion=True)


class TCellNaiveCytotoxicRecruitmentLymphRegular(RecruitmentLymph):
    def __init__(self, probability):
        RecruitmentLymph.__init__(self, probability,
                                  recruited_compartment=T_CELL_NAIVE_CYTOTOXIC)


class TCellNaiveCytotoxicRecruitmentLymphByCytokine(RecruitmentLymphByExternals):
    def __init__(self, probability):
        RecruitmentLymphByExternals.__init__(self, probability,
                                             recruited_compartment=T_CELL_NAIVE_CYTOTOXIC,
                                             external_compartments=CYTOKINE_PRODUCING_COMPARTMENTS)
