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
                                      macrophage_compartment_from=MACROPHAGE_REGULAR,
                                      macrophage_compartment_to=MACROPHAGE_ACTIVATED)


class InfectedMacrophageSpontaneousActivation(MacrophageActivation):

    def __init__(self, probability):
        MacrophageActivation.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                      macrophage_compartment_from=MACROPHAGE_INFECTED,
                                      macrophage_compartment_to=MACROPHAGE_ACTIVATED,
                                      bacteria_compartment_destroy=BACTERIA_INTRACELLULAR)


class RegularMacrophageActivationByCytokine(MacrophageActivationByExternals):

    def __init__(self, probability):
        MacrophageActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                 probability,
                                                 macrophage_compartment_from=MACROPHAGE_REGULAR,
                                                 macrophage_compartment_to=MACROPHAGE_ACTIVATED,
                                                 external_compartments=CYTOKINE_COMPARTMENTS)


class InfectedMacrophageActivationByCytokine(MacrophageActivationByExternals):

    def __init__(self, probability):
        MacrophageActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                 probability,
                                                 macrophage_compartment_from=MACROPHAGE_INFECTED,
                                                 macrophage_compartment_to=MACROPHAGE_ACTIVATED,
                                                 external_compartments=CYTOKINE_COMPARTMENTS,
                                                 bacteria_compartment_destroy=BACTERIA_INTRACELLULAR)


class ActivatedMacrophageSpontaneousDeactivation(Change):
    def __init__(self, probability):
        Change.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                        MACROPHAGE_ACTIVATED, MACROPHAGE_REGULAR)


class ActivatedMacrophageDeactivationByLackOfCytokine(MacrophageDeactivationByLackOfExternals):
    def __init__(self, probability):
        MacrophageDeactivationByLackOfExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                         probability,
                                                         macrophage_compartment_from=MACROPHAGE_ACTIVATED,
                                                         macrophage_compartment_to=MACROPHAGE_REGULAR,
                                                         external_compartments=CYTOKINE_COMPARTMENTS)
