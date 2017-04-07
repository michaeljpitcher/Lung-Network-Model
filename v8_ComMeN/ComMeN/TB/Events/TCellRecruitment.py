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


class TCellRecruitmentBronchial(RecruitmentBronchial):
    def __init__(self, probability, t_cell_compartment, based_on_perfusion=True):
        RecruitmentBronchial.__init__(self, probability, t_cell_compartment, based_on_perfusion)


class TCellRecruitmentBronchialByInfection(TCellRecruitmentBronchial):
    def __init__(self, probability, t_cell_recruited_compartment, infection_compartments, based_on_perfusion=True):
        self.infection_compartments = infection_compartments
        TCellRecruitmentBronchial.__init__(self, probability, t_cell_recruited_compartment, based_on_perfusion)

    def increment_from_node(self, node, network):
        return TCellRecruitmentBronchial.increment_from_node(self, node, network) * \
               sum([node.subpopulations[c] for c in self.infection_compartments])


class TCellRecruitmentLymph(RecruitmentLymph):
    def __init__(self, probability, t_cell_compartment):
        RecruitmentLymph.__init__(self, probability, t_cell_compartment)


class TCellRecruitmentLymphByInfection(TCellRecruitmentLymph):
    def __init__(self, probability, t_cell_compartment, infection_compartments):
        self.infection_compartments = infection_compartments,
        TCellRecruitmentLymph.__init__(self, probability, t_cell_compartment)

    def increment_from_node(self, node, network):
        return sum([node.subpopulations[c] for c in self.infection_compartments])
