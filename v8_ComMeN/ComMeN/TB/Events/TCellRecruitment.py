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


class TCellRecruitmentBronchialByInfection(RecruitmentBronchialByInfection):
    def __init__(self, probability, t_cell_recruited_compartment, infection_compartments, based_on_perfusion=True):
        RecruitmentBronchialByInfection.__init__(self, probability, t_cell_recruited_compartment, based_on_perfusion)


class TCellRecruitmentLymph(RecruitmentLymph):
    def __init__(self, probability, t_cell_compartment):
        RecruitmentLymph.__init__(self, probability, t_cell_compartment)


class TCellRecruitmentLymphByInfection(RecruitmentLymphByInfection):
    def __init__(self, probability, t_cell_compartment, infection_compartments):
        RecruitmentLymphByInfection.__init__(self, probability, t_cell_compartment)
