__author__ = "Michael J. Pitcher"

from ...Base.Event import *
from ..TBClasses import *
from ...PulmonaryAnatomy.LymphNode import *


class Recruit(Event):

    def __init__(self, class_type, node_type, probability):
        self.class_type = class_type
        self.node_type = node_type
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        if isinstance(node, self.node_type):
            return self.recruitment_basis(node)
        else:
            return 0

    def recruitment_basis(self, node):
        return 1

    def update_network(self, chosen_node, network):
        chosen_node.update(self.class_type, 1)


class RecruitByPerfusion(Recruit):

    def __init__(self, class_type, node_type, probability):
        # TODO - lymph nodes have no perfusion, maybe change this
        if node_type == LymphNode:
            raise Exception("Cannot recruit by perfusion at lymph nodes")
        Recruit.__init__(self, class_type, node_type, probability)

    def recruitment_basis(self, node):
        return node.perfusion


class RecruitByInfection(Recruit):
    def __init__(self, class_type, node_type, probability):
        Recruit.__init__(self, class_type, node_type, probability)

    def recruitment_basis(self, node):
        return node.subpopulation[MACROPHAGE_INFECTED]





