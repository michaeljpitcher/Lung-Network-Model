#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..Events.MacrophageActivation import *
from ...Base.Events.Change import *
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


class RegularMacrophageSpontaneousActivation(MacrophageActivation):

    def __init__(self, probability):
        MacrophageActivation.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                      MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED)


class InfectedMacrophageSpontaneousActivation(MacrophageActivation):

    def __init__(self, probability):
        MacrophageActivation.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                      MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED, BACTERIA_INTRACELLULAR)


class RegularMacrophageActivationByChemokine(MacrophageActivationByExternals):

    def __init__(self, probability):
        MacrophageActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                 probability, MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED,
                                                 [MACROPHAGE_INFECTED])


class InfectedMacrophageActivationByChemokine(MacrophageActivationByExternals):

    def __init__(self, probability):
        MacrophageActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                 probability, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED,
                                                 [MACROPHAGE_INFECTED], BACTERIA_INTRACELLULAR)


class RegularMacrophageActivationByTCells(MacrophageActivationByExternals):
    def __init__(self, probability):
        MacrophageActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                 probability, MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, [T_CELL])


class InfectedMacrophageActivationByTCells(MacrophageActivationByExternals):
    def __init__(self, probability):
        MacrophageActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                 probability, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED, [T_CELL],
                                                 BACTERIA_INTRACELLULAR)


class ActivatedMacrophageSpontaneousDeactivation(Change):
    def __init__(self, probability):
        Change.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                        MACROPHAGE_ACTIVATED, MACROPHAGE_REGULAR)


class ActivatedMacrophageDeactivationByLackOfInfection(MacrophageDeactivationByLackOfExternals):
    def __init__(self, probability):
        MacrophageDeactivationByLackOfExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                         probability, MACROPHAGE_ACTIVATED, MACROPHAGE_REGULAR,
                                                         [MACROPHAGE_INFECTED])

