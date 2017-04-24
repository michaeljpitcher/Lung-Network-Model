#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..TBClasses import *
from ...Base.Events.Destruction import *
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


class SpontaneousTCellHelperDeath(Destroy):
    def __init__(self, probability):
        Destroy.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability, T_CELL_HELPER)


class SpontaneousTCellCytotoxicDeath(Destroy):
    def __init__(self, probability):
        Destroy.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability, T_CELL_CYTOTOXIC)