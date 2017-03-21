__author__ = "Michael J. Pitcher"

from ...Base.Events.Create import *
from ...PulmonaryAnatomy.LymphNode import *
from ..TBClasses import *


# TODO - how is this done? Don't have perfusion in lymph nodes
class TCellRecruitedRegular(CreateAtNodeType):
    def __init__(self, probability, t_cell_type=T_CELL):
        CreateAtNodeType.__init__(self, t_cell_type, LymphNode, probability)


class TCellRecruitedThroughInfection(CreateAtNodeType):
    def __init__(self, probability, t_cell_type=T_CELL):
        CreateAtNodeType.__init__(self, t_cell_type, LymphNode, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[MACROPHAGE_INFECTED]
