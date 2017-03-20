__author__ = "Michael J. Pitcher"

from ...PulmonaryAnatomy.PulmonaryEvents.PulmonaryRecruitment import *
from ..TBClasses import *


class MacrophageRecruitmentRegular(RecruitmentThroughBloodBPS):

    def __init__(self, probability):
        RecruitmentThroughBloodBPS.__init__(self, MACROPHAGE_REGULAR, probability)


class MacrophageRecruitmentThroughInfection(RecruitmentThroughBloodBPS):

    def __init__(self, probability):
        RecruitmentThroughBloodBPS.__init__(self, MACROPHAGE_REGULAR, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[MACROPHAGE_INFECTED] * \
               RecruitmentThroughBloodBPS.increment_from_node(self, node, network)
