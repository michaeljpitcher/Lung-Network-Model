#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Pulmonary.Events.PulmonaryRecruitment import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MacrophageRecruitmentBronchial(RecruitmentBronchial):
    def __init__(self, probability, macrophage_compartment, based_on_perfusion=True):
        RecruitmentBronchial.__init__(self, probability, macrophage_compartment, based_on_perfusion)


class MacrophageRecruitmentBronchialByInfection(MacrophageRecruitmentBronchial):
    def __init__(self, probability, macrophage_recruited_compartment, infection_compartments, based_on_perfusion=True):
        self.infection_compartments = infection_compartments
        MacrophageRecruitmentBronchial.__init__(self, probability, macrophage_recruited_compartment, based_on_perfusion)

    def increment_from_node(self, node, network):
        return sum([node.subpopulations[c] for c in self.infection_compartments]) * \
               MacrophageRecruitmentBronchial.increment_from_node(self, node, network)


class MacrophageRecruitmentLymph(RecruitmentLymph):
    def __init__(self, probability, macrophage_compartment):
        RecruitmentLymph.__init__(self, probability, macrophage_compartment)


class MacrophageRecruitmentLymphByInfection(MacrophageRecruitmentLymph):
    def __init__(self, probability, macrophage_recruited_compartment, infection_compartments):
        self.infection_compartments = infection_compartments
        MacrophageRecruitmentLymph.__init__(self, probability, macrophage_recruited_compartment)

    def increment_from_node(self, node, network):
        return sum([node.subpopulations[c] for c in self.infection_compartments])
