#!/usr/bin/env python

"""Bacteria change metabolism

Bacteria can change their metabolism based on the oxygen availability in their current location.

"""

from ...Pulmonary.Events.PulmonaryChange import *
from ..TBClasses import *
from ...Pulmonary.Node.BronchopulmonarySegment import *
from ...Pulmonary.Node.BronchialTreeNode import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"
# TODO - other change methods


class BacteriaChangeByOxygenFastToSlow(ChangeByOxygen):
    """
    A fast bacterium changes to slow, greater chance the less oxygen there is
    """
    def __init__(self, probability):
        # Not at lymph node - no oxygen availability value there
        ChangeByOxygen.__init__(self, [BronchialTreeNode, BronchopulmonarySegment], probability,
                                compartment_from=BACTERIA_FAST,
                                compartment_to=BACTERIA_SLOW,
                                oxygen_high_to_change=False)


class BacteriaChangeByOxygenSlowToFast(ChangeByOxygen):
    """
    A slow bacterium changes to fast, greater chance the more oxygen there is
    """
    def __init__(self, probability):
        # Not at lymph node - no oxygen availability value there
        ChangeByOxygen.__init__(self, [BronchialTreeNode, BronchopulmonarySegment], probability,
                                compartment_from=BACTERIA_SLOW,
                                compartment_to=BACTERIA_FAST,
                                oxygen_high_to_change=True)
