#!/usr/bin/env python

""" Macrophage activation/deactivation

A macrophage enters an activated state increasing it's bactericidal activity. If the macrophage is infected, also causes 
destruction of internal bacteria.

Activated macrophages can deactivated and thus return to regular
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
                        internals_to_destroy=[BACTERIA_INTRACELLULAR])


class RegularMacrophageActivationByCytokine(ChangeByOtherCompartments):
    """
    Macrophage becomes activated due to its exposure to cytokine, produced by other entities (e.g. infected/activated 
    macrophages)
    """
    def __init__(self, probability):
        ChangeByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                           probability,
                                           compartment_from=MACROPHAGE_REGULAR,
                                           compartment_to=MACROPHAGE_ACTIVATED,
                                           influencing_compartments=CYTOKINE_PRODUCING_COMPARTMENTS)


class InfectedMacrophageActivationByCytokine(ChangeByOtherCompartments):
    def __init__(self, probability):
        ChangeByOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                           probability,
                                           compartment_from=MACROPHAGE_INFECTED,
                                           compartment_to=MACROPHAGE_ACTIVATED,
                                           influencing_compartments=CYTOKINE_PRODUCING_COMPARTMENTS,
                                           internals_to_destroy=[BACTERIA_INTRACELLULAR])


class ActivatedMacrophageSpontaneousDeactivation(Change):
    def __init__(self, probability):
        Change.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode], probability,
                        compartment_from=MACROPHAGE_ACTIVATED,
                        compartment_to=MACROPHAGE_REGULAR)


class ActivatedMacrophageDeactivationByLackOfCytokine(ChangeByLackOfOtherCompartments):
    """
    Activated macrophage reverts to normal (more likely the less cytokine producing compartments there are)
    """
    def __init__(self, probability):
        ChangeByLackOfOtherCompartments.__init__(self, [BronchopulmonarySegment, BronchialTreeNode, LymphNode],
                                                 probability,
                                                 compartment_from=MACROPHAGE_ACTIVATED,
                                                 compartment_to=MACROPHAGE_REGULAR,
                                                 influencing_compartments=CYTOKINE_PRODUCING_COMPARTMENTS)
