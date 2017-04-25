#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Change import ChangeByOtherCompartments
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


class MacrophageRegularActivationByTCellHelper(ChangeByOtherCompartments):
    def __init__(self, probability):
        ChangeByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                           probability,
                                           compartment_from=MACROPHAGE_REGULAR,
                                           compartment_to=MACROPHAGE_ACTIVATED,
                                           influencing_compartments=[T_CELL_HELPER])


class MacrophageInfectedActivationByTCellHelper(ChangeByOtherCompartments):
    def __init__(self, probability):
        ChangeByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                           probability,
                                           compartment_from=MACROPHAGE_INFECTED,
                                           compartment_to=MACROPHAGE_ACTIVATED,
                                           influencing_compartments=[T_CELL_HELPER],
                                           internals_to_destroy=[BACTERIA_INTRACELLULAR])
