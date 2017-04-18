#!/usr/bin/env python

"""Short docstring

Long Docstring

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


class BacteriaReplicationFast(Replication):
    def __init__(self, probability):
        Replication.__init__(self, [BronchialTreeNode, BronchopulmonarySegment, LymphNode], probability, BACTERIA_FAST)


class BacteriaReplicationSlow(Replication):
    def __init__(self, probability):
        Replication.__init__(self, [BronchialTreeNode, BronchopulmonarySegment, LymphNode], probability, BACTERIA_SLOW)


class BacteriaReplicationIntracellular(Replication):
    def __init__(self, probability):
        Replication.__init__(self, [BronchialTreeNode, BronchopulmonarySegment, LymphNode], probability,
                             BACTERIA_INTRACELLULAR)
