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
                                 macrophage_compartment=MACROPHAGE_REGULAR)


class InfectedMacrophageSpontaneousDeath(MacrophageDeath):
    def __init__(self, probability):
        MacrophageDeath.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                 macrophage_compartment=MACROPHAGE_INFECTED,
                                 internal_bacteria_compartment=BACTERIA_INTRACELLULAR,
                                 bacteria_release_compartment_to=BACTERIA_SLOW)


class ActivatedMacrophageSpontaneousDeath(MacrophageDeath):
    def __init__(self, probability):
        MacrophageDeath.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                 macrophage_compartment=MACROPHAGE_ACTIVATED)


# NECROSIS
class InfectedMacrophageDeathByIntracellularBacteria(MacrophageDeathByOtherCompartments):
    def __init__(self, probability):
        MacrophageDeathByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                                    macrophage_compartment=MACROPHAGE_INFECTED,
                                                    death_causing_compartments=[BACTERIA_INTRACELLULAR],
                                                    internal_bacteria_compartment=BACTERIA_INTRACELLULAR,
                                                    bacteria_release_compartment_to=BACTERIA_SLOW)
