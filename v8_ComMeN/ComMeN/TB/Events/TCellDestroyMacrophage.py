#!/usr/bin/env python

""" Cytotoxic t-cell causes apoptosis in infected macrophage

Cytotoxic t-cell comes into contact with infected macrophage, triggers apoptosis which destroys both the
macrophage and its internal bacterial load.

"""

from ...Base.Events.Destruction import *
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


class TCellCytotoxicDestroysInfectedMacrophage(DestroyByOtherCompartments):
    # TODO - kills all internal bacteria not T-cell - check this, may need two events or more
    def __init__(self, probability):
        DestroyByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                            compartment_destroyed=MACROPHAGE_INFECTED,
                                            influencing_compartments=[T_CELL_CYTOTOXIC],
                                            internals_to_destroy=[BACTERIA_INTRACELLULAR])
