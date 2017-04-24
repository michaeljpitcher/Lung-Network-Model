#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Pulmonary.Events.PhagocyteDeath import *
from ..TBClasses import *
from ...Pulmonary.Node.BronchialTreeNode import *
from ...Pulmonary.Node.BronchopulmonarySegment import *
from ...Pulmonary.Node.LymphNode import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TCellCytotoxicDestroysInfectedMacrophage(PhagocyteDeathByOtherCompartments):
    # TODO - kills all internal bacteria not T-cell - check this, may need two events or more
    def __init__(self, probability):
        PhagocyteDeathByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                                   phagocyte_compartment=MACROPHAGE_INFECTED,
                                                   death_causing_compartments=[T_CELL_CYTOTOXIC],
                                                   extra_compartments_to_destroy=[],
                                                   internal_compartment=BACTERIA_INTRACELLULAR)