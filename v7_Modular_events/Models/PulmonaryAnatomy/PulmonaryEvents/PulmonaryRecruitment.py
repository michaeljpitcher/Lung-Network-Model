__author__ = "Michael J. Pitcher"

from ...Base.Events.Create import *
from ..BronchopulmonarySegment import *


class RecruitmentThroughBloodBPS(Create):

    def __init__(self, type_recruited, probability):
        Create.__init__(self, type_recruited, probability)

    def increment_from_node(self, node, network):
        if isinstance(node, BronchopulmonarySegment):
            return node.perfusion
        else:
            return 0