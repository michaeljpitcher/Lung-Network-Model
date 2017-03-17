__author__ = "Michael J. Pitcher"

from ...Base.Events.Create import *


class RecruitmentThroughBlood(Create):

    def __init__(self, type_recruited, probability):
        Create.__init__(self, type_recruited, probability)

    def increment_from_node(self, node, network):
        return node.perfusion
