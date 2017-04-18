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


class TCellTranslocateBronchus(TranslocateBronchus):

    def __init__(self, node_types, probability, t_cell_compartment, edge_choice_based_on_weight=False):
        TranslocateBronchus.__init__(self, node_types, probability, t_cell_compartment, edge_choice_based_on_weight)


class TCellTranslocateLymph(TranslocateLymph):

    def __init__(self, node_types, probability, t_cell_compartment, direction_only=True):
        TranslocateLymph.__init__(self, node_types, probability, t_cell_compartment, direction_only)
