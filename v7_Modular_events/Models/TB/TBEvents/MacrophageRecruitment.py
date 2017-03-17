__author__ = "Michael J. Pitcher"

from ...PulmonaryAnatomy.PulmonaryEvents.PulmonaryRecruitment import *
from ..TBClasses import *


class MacrophageRecruitmentRegular(RecruitmentThroughBlood):

    def __init__(self, probability):
        RecruitmentThroughBlood.__init__(self, MACROPHAGE_REGULAR, probability)


class MacrophageRecruitmentThroughInfection(RecruitmentThroughBlood):

    def __init__(self, probability):
        RecruitmentThroughBlood.__init__(self, MACROPHAGE_REGULAR, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[MACROPHAGE_INFECTED] * node.perfusion
