#!/usr/bin/env python

""" Dendritic Cell translocation

A dendritic cell can move from a bronchopulmonary segment into a lymph node.

"""

from ...Pulmonary.Events.PulmonaryTranslocate import *
from ...Pulmonary.Node.BronchopulmonarySegment import *
from ..TBClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class DendriticImmatureLymphTranslocation(TranslocateLymph):
    def __init__(self, probability):
        # Translocation is only bronchopulmonary segment to lymph
        TranslocateLymph.__init__(self, [BronchopulmonarySegment], probability,
                                  translocate_compartment=DENDRITIC_CELL_IMMATURE,
                                  flow_based=True)


class DendriticMatureLymphTranslocation(TranslocateLymph):
    def __init__(self, probability):
        TranslocateLymph.__init__(self, [BronchopulmonarySegment], probability,
                                  translocate_compartment=DENDRITIC_CELL_MATURE,
                                  flow_based=True)
