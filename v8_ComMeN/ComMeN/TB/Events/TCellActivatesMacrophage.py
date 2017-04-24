#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Pulmonary.Events.PhagocyteActivation import *
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


class MacrophageRegularActivationByTCellHelper(PhagocyteActivationByExternals):
    def __init__(self, probability):
        PhagocyteActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                probability,
                                                phagocyte_compartment_from=MACROPHAGE_REGULAR,
                                                phagocyte_compartment_to=MACROPHAGE_ACTIVATED,
                                                external_compartments=[T_CELL_HELPER])


class MacrophageInfectedActivationByTCellHelper(PhagocyteActivationByExternals):
    def __init__(self, probability):
        PhagocyteActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                probability,
                                                phagocyte_compartment_from=MACROPHAGE_INFECTED,
                                                phagocyte_compartment_to=MACROPHAGE_ACTIVATED,
                                                external_compartments=[T_CELL_HELPER],
                                                bacteria_compartment_destroy=BACTERIA_INTRACELLULAR)