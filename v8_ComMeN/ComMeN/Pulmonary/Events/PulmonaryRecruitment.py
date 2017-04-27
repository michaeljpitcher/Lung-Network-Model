#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Creation import *
from ..Node.BronchopulmonarySegment import *
from ..Node.BronchialTreeNode import *
from ..Node.LymphNode import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class RecruitmentBronchial(Create):

    def __init__(self, probability, recruited_compartment, based_on_perfusion=True):
        node_types = [BronchopulmonarySegment, BronchialTreeNode]
        self.based_on_perfusion = based_on_perfusion
        Create.__init__(self, node_types, probability, recruited_compartment)

    def increment_state_variable_from_node(self, node, network):
        if self.based_on_perfusion:
            return node.perfusion
        else:
            return Create.increment_state_variable_from_node(self, node, network)


class RecruitmentBronchialByExternals(RecruitmentBronchial):

    def __init__(self, probability, recruited_compartment, external_compartments, based_on_perfusion=True):
        self.external_compartments = external_compartments
        RecruitmentBronchial.__init__(self, probability, recruited_compartment, based_on_perfusion)

    def increment_state_variable_from_node(self, node, network):
        return RecruitmentBronchial.increment_state_variable_from_node(self, node, network) * \
               sum([node.subpopulations[c] for c in self.external_compartments])


class RecruitmentLymph(Create):

    def __init__(self, probability, recruited_compartment):
        node_types = [LymphNode]
        Create.__init__(self, node_types, probability, recruited_compartment)


class RecruitmentLymphByExternals(RecruitmentLymph):
    def __init__(self, probability, recruited_compartment, external_compartments):
        self.external_compartments = external_compartments
        RecruitmentLymph.__init__(self, probability, recruited_compartment)

    def increment_state_variable_from_node(self, node, network):
        return RecruitmentLymph.increment_state_variable_from_node(self, node, network) * \
               sum([node.subpopulations[c] for c in self.external_compartments])
