__author__ = "Michael J. Pitcher"

from ...Base.Events.Change import *
from ..TBClasses import *


class MacrophageActivation(Change):
    """
    Spontaneous activation
    """

    def __init__(self, probability):
        Change.__init__(self, MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, probability)


class MacrophageActivationThroughInfection(ChangeThroughOtherClass):
    """
    Activation through infection levels (chemokine)
    """
    def __init__(self, probability):
        ChangeThroughOtherClass.__init__(self, class_from=MACROPHAGE_REGULAR, class_to=MACROPHAGE_ACTIVATED,
                                         influencing_class=MACROPHAGE_INFECTED, probability=probability)


class MacrophageActivationThroughTCell(ChangeThroughOtherClass):
    """
    Activation through infection levels (chemokine)
    """
    def __init__(self, probability):
        ChangeThroughOtherClass.__init__(self, class_from=MACROPHAGE_REGULAR, class_to=MACROPHAGE_ACTIVATED,
                                         influencing_class=T_CELL, probability=probability)


class MacrophageDeactivation(Change):
    """
    Spontaneous deactivation
    """

    def __init__(self, probability):
        Change.__init__(self, MACROPHAGE_ACTIVATED, MACROPHAGE_REGULAR, probability)

# TODO - other means of macrophage deactivation