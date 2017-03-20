__author__ = "Michael J. Pitcher"

from ...PulmonaryAnatomy.PulmonaryEvents.PulmonaryRecruitment import *
from ..TBClasses import *


class TCellRecruitmentRegular(RecruitmentThroughBloodBPS):

    def __init__(self, t_cell_type, probability):
        RecruitmentThroughBloodBPS.__init__(self, t_cell_type, probability)


class TCellRecruitmentThroughInfection(RecruitmentThroughBloodBPS):

    def __init__(self, probability):
        RecruitmentThroughBloodBPS.__init__(self, MACROPHAGE_REGULAR, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[MACROPHAGE_INFECTED] * \
               RecruitmentThroughBloodBPS.increment_from_node(self, node, network)
