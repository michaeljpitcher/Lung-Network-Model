#!/usr/bin/env python

""" Macrophage death

A macrophage dies. If infected, may release it's internal bacterial load as extracellular slow bacteria

"""

from ...Base.Events.Destruction import *
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


class RegularMacrophageSpontaneousDeath(Destroy):
    def __init__(self, probability):
        Destroy.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                         compartment_destroyed=MACROPHAGE_REGULAR)


class InfectedMacrophageSpontaneousDeath(Destroy):
    """
    Infected macrophages does, intracellular bacteria become extracellular slow bacteria
    """
    def __init__(self, probability):
        Destroy.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                         compartment_destroyed=MACROPHAGE_INFECTED,
                         internals_changed=[(BACTERIA_INTRACELLULAR, BACTERIA_SLOW)])


class ActivatedMacrophageSpontaneousDeath(Destroy):
    def __init__(self, probability):
        Destroy.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                         compartment_destroyed=MACROPHAGE_ACTIVATED)


# NECROSIS
class InfectedMacrophageDeathByIntracellularBacteria(DestroyByOtherCompartments):
    """
    Infected macrophage dies, where death is instigated by internal bacteria (the more intracellular bacteria, the more 
    likely death occurs)
    """
    def __init__(self, probability):
        DestroyByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                            compartment_destroyed=MACROPHAGE_INFECTED,
                                            influencing_compartments=[BACTERIA_INTRACELLULAR],
                                            internals_changed=[(BACTERIA_INTRACELLULAR, BACTERIA_SLOW)])
