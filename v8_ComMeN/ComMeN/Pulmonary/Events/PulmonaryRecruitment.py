#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Creation import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class RecruitmentBronchial(Create):

    def __init__(self, node_types, probability, recruited_compartment, based_on_perfusion=True):
        self.based_on_perfusion = based_on_perfusion
        Create.__init__(self, node_types, probability, recruited_compartment)

    def increment_from_node(self, node, network):
        if self.based_on_perfusion:
            return node.perfusion
        else:
            return Create.increment_from_node(self, node, network)


class RecruitmentBronchialByInfection(RecruitmentBronchial):

    def __init__(self, node_types, probability, recruited_compartment, infection_compartments, based_on_perfusion=True):
        self.infection_compartments = infection_compartments
        RecruitmentBronchial.__init__(self, node_types, probability, recruited_compartment, based_on_perfusion)

    def increment_from_node(self, node, network):
        return RecruitmentBronchial.increment_from_node(self, node, network) * \
               sum([node.subpopulations[c] for c in self.infection_compartments])


class RecruitmentLymph(Create):

    def __init__(self, node_types, probability, recruited_compartment):
        Create.__init__(self, node_types, probability, recruited_compartment)


class RecruitmentLymphByInfection(RecruitmentLymph):
    def __init__(self, node_types, probability, recruited_compartment, infection_compartments):
        self.infection_compartments = infection_compartments
        RecruitmentLymph.__init__(self, node_types, probability, recruited_compartment)

    def increment_from_node(self, node, network):
        return RecruitmentLymph.increment_from_node(self, node, network) * \
               sum([node.subpopulations[c] for c in self.infection_compartments])
