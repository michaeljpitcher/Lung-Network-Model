#!/usr/bin/env python

"""Short docstring

Long Docstring

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


class TCellHelperRecruitmentBronchialRegular(RecruitmentBronchial):
    def __init__(self, probability):
        RecruitmentBronchial.__init__(self, [BronchialTreeNode, BronchopulmonarySegment], probability, T_CELL_HELPER, True)


class TCellHelperRecruitmentBronchialThroughInfection(RecruitmentBronchialByExternals):
    def __init__(self, probability):
        RecruitmentBronchialByExternals.__init__(self, [BronchialTreeNode, BronchopulmonarySegment], probability,
                                                 T_CELL_HELPER, [MACROPHAGE_INFECTED], True)


class TCellHelperRecruitmentLymphRegular(RecruitmentLymph):
    def __init__(self, probability):
        RecruitmentLymph.__init__(self, [LymphNode], probability, T_CELL_HELPER)


class TCellHelperRecruitmentLymphThroughInfection(RecruitmentLymphByExternals):
    def __init__(self, probability):
        RecruitmentLymphByExternals.__init__(self, [LymphNode], probability, T_CELL_HELPER, [MACROPHAGE_INFECTED])


class TCellCytotoxicRecruitmentBronchialRegular(RecruitmentBronchial):
    def __init__(self, probability):
        RecruitmentBronchial.__init__(self, [BronchialTreeNode, BronchopulmonarySegment], probability, T_CELL_CYTOTOXIC,
                                      True)


class TCellCytotoxicRecruitmentBronchialThroughInfection(RecruitmentBronchialByExternals):
    def __init__(self, probability):
        RecruitmentBronchialByExternals.__init__(self, [BronchialTreeNode, BronchopulmonarySegment], probability,
                                                 T_CELL_CYTOTOXIC, [MACROPHAGE_INFECTED], True)


class TCellCytotoxicRecruitmentLymphRegular(RecruitmentLymph):
    def __init__(self, probability):
        RecruitmentLymph.__init__(self, [LymphNode], probability, T_CELL_CYTOTOXIC)


class TCellCytotoxicRecruitmentLymphThroughInfection(RecruitmentLymphByExternals):
    def __init__(self, probability):
        RecruitmentLymphByExternals.__init__(self, [LymphNode], probability, T_CELL_CYTOTOXIC, [MACROPHAGE_INFECTED])
