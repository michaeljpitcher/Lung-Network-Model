#!/usr/bin/env python

""" Dendritic cell recruitment

Dendritic cell is recruited into the patch

"""

from ...Pulmonary.Events.PulmonaryRecruitment import *
from ..TBClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class DendriticImmatureRecruitmentBronchial(RecruitmentBronchial):
    """
    Dendritic cell recruited into the bronchial tree. Based on perfusion rates.
    """
    def __init__(self, probability):
        RecruitmentBronchial.__init__(self, probability,
                                      recruited_compartment=DENDRITIC_CELL_IMMATURE,
                                      based_on_perfusion=True)


class DendriticImmatureRecruitmentLymph(RecruitmentLymph):
    def __init__(self, probability):
        RecruitmentLymph.__init__(self, probability,
                                  recruited_compartment=DENDRITIC_CELL_IMMATURE)
