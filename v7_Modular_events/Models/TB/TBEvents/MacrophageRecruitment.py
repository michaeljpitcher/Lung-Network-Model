__author__ = "Michael J. Pitcher"

from ...PulmonaryAnatomy.PulmonaryEvents.PulmonaryRecruitment import *
from ..TBClasses import *
from ...PulmonaryAnatomy.LymphNode import *

# TODO - better methods of recruitment, involving less individual classes


class MacrophageRecruitmentRegularBPS(RecruitmentThroughBloodBPS):
    def __init__(self, probability, macrophage_type=MACROPHAGE_REGULAR):
        RecruitmentThroughBloodBPS.__init__(self, macrophage_type, probability)


class MacrophageRecruitmentThroughInfectionBPS(RecruitmentThroughBloodBPS):
    def __init__(self, probability, macrophage_type=MACROPHAGE_REGULAR):
        RecruitmentThroughBloodBPS.__init__(self, macrophage_type, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[MACROPHAGE_INFECTED] * \
               RecruitmentThroughBloodBPS.increment_from_node(self, node, network)


# TODO - macrophage in lymph. No perfusion in lymph
class MacrophageRecruitmentRegularLymph(CreateAtNodeType):
    def __init__(self, probability, macrophage_type=MACROPHAGE_REGULAR):
        CreateAtNodeType.__init__(self, macrophage_type, LymphNode, probability)


class MacrophageRecruitmentThroughInfectionLymph(CreateAtNodeType):
    def __init__(self, probability, macrophage_type=MACROPHAGE_REGULAR):
        CreateAtNodeType.__init__(self, macrophage_type, LymphNode, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[MACROPHAGE_INFECTED]
