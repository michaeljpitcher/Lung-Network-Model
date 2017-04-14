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
    def __init__(self, node_types, probability, macrophage_compartment, based_on_perfusion=True):
        RecruitmentBronchial.__init__(self, node_types, probability, macrophage_compartment, based_on_perfusion)


class MacrophageRecruitmentBronchialByInfection(RecruitmentBronchialByInfection):
    def __init__(self, node_types, probability, macrophage_recruited_compartment, infection_compartments, based_on_perfusion=True):
        RecruitmentBronchialByInfection.__init__(self, node_types, probability, macrophage_recruited_compartment,
                                                 infection_compartments, based_on_perfusion)


class MacrophageRecruitmentLymph(RecruitmentLymph):
    def __init__(self, node_types, probability, macrophage_compartment):
        RecruitmentLymph.__init__(self, node_types, probability, macrophage_compartment)


class MacrophageRecruitmentLymphByInfection(RecruitmentLymphByInfection):
    def __init__(self, node_types, probability, macrophage_recruited_compartment, infection_compartments):
        RecruitmentLymphByInfection.__init__(self, node_types, probability, infection_compartments,
                                             macrophage_recruited_compartment)
