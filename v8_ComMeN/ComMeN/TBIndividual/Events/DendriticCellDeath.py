#!/usr/bin/env python

""" Dendritic cell death

A dendritic cell dies

"""

from ...Base.Events.Destruction import *
from ..TBClasses import *
# TODO - maybe a way to have cell types as "ALL" so no need to import all the time
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


class DendriticImmatureDeath(Destroy):
    def __init__(self, probability):
        Destroy.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                         compartment_destroyed=DENDRITIC_CELL_IMMATURE)


class DendriticMatureDeath(Destroy):
    def __init__(self, probability):
        Destroy.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                         compartment_destroyed=DENDRITIC_CELL_MATURE)
