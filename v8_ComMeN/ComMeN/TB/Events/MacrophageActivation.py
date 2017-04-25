#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

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


class RegularMacrophageSpontaneousActivation(Change):

    def __init__(self, probability):
        Change.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                     compartment_from=MACROPHAGE_REGULAR,
                                     compartment_to=MACROPHAGE_ACTIVATED)


class InfectedMacrophageSpontaneousActivation(Change):

    def __init__(self, probability):
        Change.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                                     compartment_from=MACROPHAGE_INFECTED,
                                     compartment_to=MACROPHAGE_ACTIVATED,
                                     internals_to_destroy=BACTERIA_INTRACELLULAR)


class RegularMacrophageActivationByCytokine(ChangeByOtherCompartments):

    def __init__(self, probability):
        ChangeByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                           probability,
                                           compartment_from=MACROPHAGE_REGULAR,
                                           compartment_to=MACROPHAGE_ACTIVATED,
                                           influencing_compartments=CYTOKINE_COMPARTMENTS)


class InfectedMacrophageActivationByCytokine(ChangeByOtherCompartments):

    def __init__(self, probability):
        ChangeByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                           probability,
                                           compartment_from=MACROPHAGE_INFECTED,
                                           compartment_to=MACROPHAGE_ACTIVATED,
                                           influencing_compartments=CYTOKINE_COMPARTMENTS,
                                           internals_to_destroy=BACTERIA_INTRACELLULAR)


class ActivatedMacrophageSpontaneousDeactivation(Change):
    def __init__(self, probability):
        Change.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                        MACROPHAGE_ACTIVATED, MACROPHAGE_REGULAR)


class ActivatedMacrophageDeactivationByLackOfCytokine(ChangeByLackOfOtherCompartments):
    def __init__(self, probability):
        ChangeByLackOfOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                        probability,
                                                        compartment_from=MACROPHAGE_ACTIVATED,
                                                        compartment_to=MACROPHAGE_REGULAR,
                                                        influencing_compartments=CYTOKINE_COMPARTMENTS)
