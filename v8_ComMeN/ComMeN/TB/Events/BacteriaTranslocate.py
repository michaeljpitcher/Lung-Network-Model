#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Pulmonary.Events.PulmonaryTranslocate import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class BacteriaTranslocateBronchus(TranslocateBronchus):

    def __init__(self, probability, bacteria_compartment, edge_choice_based_on_weight=False):
        TranslocateBronchus.__init__(self, probability, bacteria_compartment, edge_choice_based_on_weight)


class BacteriaTranslocateLymph(TranslocateLymph):

    def __init__(self, probability, bacteria_compartment, direction_only=True):
        TranslocateLymph.__init__(self, probability, bacteria_compartment, direction_only)
