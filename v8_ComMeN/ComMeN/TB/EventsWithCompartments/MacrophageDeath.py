#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..Events.MacrophageDeath import *
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


class RegularMacrophageSpontaneousDeath(MacrophageDeath):
    def __init__(self, probability):
        MacrophageDeath.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                 MACROPHAGE_REGULAR)


class InfectedMacrophageSpontaneousDeath(MacrophageDeath):
    def __init__(self, probability):
        MacrophageDeath.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                 MACROPHAGE_INFECTED, BACTERIA_INTRACELLULAR, BACTERIA_SLOW)


class ActivatedMacrophageSpontaneousDeath(MacrophageDeath):
    def __init__(self, probability):
        MacrophageDeath.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                 MACROPHAGE_ACTIVATED)


# NECROSIS
class InfectedMacrophageDeathByIntracellularBacteria(MacrophageDeathByExternals):
    def __init__(self, probability):
        MacrophageDeathByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                            MACROPHAGE_INFECTED, [BACTERIA_INTRACELLULAR],
                                            internal_bacteria_compartment=BACTERIA_INTRACELLULAR,
                                            bacteria_release_compartment_to=BACTERIA_SLOW)
