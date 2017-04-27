#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Phagocytosis import *
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
# TODO - bacteria can't survive this (like they do in macs). Maybe need an infected dendritic?


class ImmatureDendriticIngestFastBacteriaMaturate(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=DENDRITIC_CELL_IMMATURE,
                              compartment_to_ingest=BACTERIA_FAST,
                              compartment_to_change_phagocyte_to=DENDRITIC_CELL_MATURE)


class ImmatureDendriticIngestSlowBacteriaMaturate(Phagocytosis):
    def __init__(self, probability):
        Phagocytosis.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                              phagocyte_compartment=DENDRITIC_CELL_IMMATURE,
                              compartment_to_ingest=BACTERIA_SLOW,
                              compartment_to_change_phagocyte_to=DENDRITIC_CELL_MATURE)