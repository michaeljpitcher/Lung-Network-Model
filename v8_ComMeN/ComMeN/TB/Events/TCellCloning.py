#!/usr/bin/env python

""" T-cell clonal expansion

Effector T-cell clones itself, creating a t-cell of same type 

"""

from ...Base.Events.Creation import *
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


class TCellHelperCloning(Replication):
    def __init__(self, probability):
        Replication.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                             T_CELL_HELPER)


class TCellCytotoxicCloning(Replication):
    def __init__(self, probability):
        Replication.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                             T_CELL_CYTOTOXIC)
