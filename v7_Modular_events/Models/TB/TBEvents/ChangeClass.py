__author__ = "Michael J. Pitcher"

from v7_Modular_events.Models.Base.Events.Change import *
from ..TBClasses import *
from ...PulmonaryAnatomy.BronchopulmonarySegment import *


class ChangeMetabolismByOxygen(Change):

    def __init__(self, original_metabolism, probability):
        if original_metabolism == BACTERIA_FAST:
            new_metabolism = BACTERIA_SLOW
        else:
            new_metabolism = BACTERIA_FAST
        Change.__init__(self, original_metabolism, new_metabolism, probability)

    def increment_from_node(self, node, network):
        if isinstance(node, BronchopulmonarySegment):
            if self.class_from == BACTERIA_SLOW:
                return node.subpopulations[BACTERIA_SLOW] * node.oxygen_tension
            else:
                return node.subpopulations[BACTERIA_FAST] * (1/node.oxygen_tension)
        else:
            return 0


class ActivateMacrophageByTCell(ChangeClassThroughOtherClass):

    def __init__(self, macrophage_state, probability, destroy_load=True):
        self.destroy_load = destroy_load
        ChangeClassThroughOtherClass.__init__(self, macrophage_state, MACROPHAGE_ACTIVATED, T_CELL, probability)


class ActivateMacrophageByInfection(ChangeClassThroughOtherClass):

    def __init__(self, macrophage_state, probability, destroy_load=True):
        self.destroy_load = destroy_load
        ChangeClassThroughOtherClass.__init__(self, macrophage_state, MACROPHAGE_ACTIVATED, MACROPHAGE_INFECTED,
                                              probability)


class DeactivateMacrophage(Change):

    def __init__(self, probability):
        # TODO - what causes macrophage to deactivate?
        Change.__init__(self, MACROPHAGE_ACTIVATED, MACROPHAGE_REGULAR, probability)
