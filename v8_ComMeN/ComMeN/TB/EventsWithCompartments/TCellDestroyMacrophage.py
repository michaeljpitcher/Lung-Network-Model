#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..Events.MacrophageDeath import *
from ..TBClasses import *
from ...Pulmonary.Node.BronchopulmonarySegment import *
from ...Pulmonary.Node.BronchialTreeNode import *
from ...Pulmonary.Node.LymphNode import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TCellDestroysInfectedMacrophage(MacrophageDeathByExternals):
    # TODO - kills all internal bacteria not T-cell - check this, may need two events or more
    def __init__(self, probability):
        MacrophageDeathByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                            macrophage_compartment=MACROPHAGE_INFECTED,
                                            external_compartments=[T_CELL_CYTOTOXIC],
                                            externals_to_destroy=[],
                                            internal_bacteria_compartment=BACTERIA_INTRACELLULAR)