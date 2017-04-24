#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..Events.MacrophageActivation import *
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


class MacrophageRegularActivationByTCellHelper(MacrophageActivationByExternals):
    def __init__(self, probability):
        MacrophageActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                 probability,
                                                 macrophage_compartment_from=MACROPHAGE_REGULAR,
                                                 macrophage_compartment_to=MACROPHAGE_ACTIVATED,
                                                 external_compartments=[T_CELL_HELPER])


class MacrophageInfectedActivationByTCellHelper(MacrophageActivationByExternals):
    def __init__(self, probability):
        MacrophageActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                 probability,
                                                 macrophage_compartment_from=MACROPHAGE_INFECTED,
                                                 macrophage_compartment_to=MACROPHAGE_ACTIVATED,
                                                 external_compartments=[T_CELL_HELPER],
                                                 bacteria_compartment_destroy=BACTERIA_INTRACELLULAR)