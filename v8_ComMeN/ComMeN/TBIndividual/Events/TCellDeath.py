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


class TCellNaiveHelperSpontaneousDeath(Destroy):
    def __init__(self, probability):
        Destroy.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                         compartment_destroyed=T_CELL_NAIVE_HELPER)


class TCellNaiveCytotoxicSpontaneousDeath(Destroy):
    def __init__(self, probability):
        Destroy.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                         compartment_destroyed=T_CELL_NAIVE_CYTOTOXIC)


class TCellHelperSpontaneousDeath(Destroy):
    def __init__(self, probability):
        Destroy.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                         compartment_destroyed=T_CELL_HELPER)


class TCellCytotoxicSpontaneousDeath(Destroy):
    def __init__(self, probability):
        Destroy.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                         compartment_destroyed=T_CELL_CYTOTOXIC)