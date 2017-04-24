#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Pulmonary.Events.PhagocyteActivation import *
from ..TBClasses import *
from ...Base.Events.Change import *
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


class RegularMacrophageSpontaneousActivation(PhagocyteActivation):

    def __init__(self, probability):
        PhagocyteActivation.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                     phagocyte_compartment_from=MACROPHAGE_REGULAR,
                                     phagocyte_compartment_to=MACROPHAGE_ACTIVATED)


class InfectedMacrophageSpontaneousActivation(PhagocyteActivation):

    def __init__(self, probability):
        PhagocyteActivation.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                     phagocyte_compartment_from=MACROPHAGE_INFECTED,
                                     phagocyte_compartment_to=MACROPHAGE_ACTIVATED,
                                     bacteria_compartment_destroy=BACTERIA_INTRACELLULAR)


class RegularMacrophageActivationByCytokine(PhagocyteActivationByExternals):

    def __init__(self, probability):
        PhagocyteActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                probability,
                                                phagocyte_compartment_from=MACROPHAGE_REGULAR,
                                                phagocyte_compartment_to=MACROPHAGE_ACTIVATED,
                                                external_compartments=CYTOKINE_COMPARTMENTS)


class InfectedMacrophageActivationByCytokine(PhagocyteActivationByExternals):

    def __init__(self, probability):
        PhagocyteActivationByExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                probability,
                                                phagocyte_compartment_from=MACROPHAGE_INFECTED,
                                                phagocyte_compartment_to=MACROPHAGE_ACTIVATED,
                                                external_compartments=CYTOKINE_COMPARTMENTS,
                                                bacteria_compartment_destroy=BACTERIA_INTRACELLULAR)


class ActivatedMacrophageSpontaneousDeactivation(Change):
    def __init__(self, probability):
        Change.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                        MACROPHAGE_ACTIVATED, MACROPHAGE_REGULAR)


class ActivatedMacrophageDeactivationByLackOfCytokine(PhagocyteDeactivationByLackOfExternals):
    def __init__(self, probability):
        PhagocyteDeactivationByLackOfExternals.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                        probability,
                                                        phagocyte_compartment_from=MACROPHAGE_ACTIVATED,
                                                        phagocyte_compartment_to=MACROPHAGE_REGULAR,
                                                        external_compartments=CYTOKINE_COMPARTMENTS)
