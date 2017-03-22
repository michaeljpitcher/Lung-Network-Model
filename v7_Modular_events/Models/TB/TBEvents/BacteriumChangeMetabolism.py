__author__ = "Michael J. Pitcher"

from ...PulmonaryAnatomy.PulmonaryEvents.PulmonaryChange import *
from ..TBClasses import *


class BacteriumChangeMetabolism(ChangeByOxygenBPS):

    def __init__(self, bacterium_metabolism_from, bacterium_metabolism_to, probability):
        if bacterium_metabolism_from == BACTERIA_FAST and bacterium_metabolism_to == BACTERIA_SLOW:
            oxygen_high = False
        else:
            oxygen_high = True
        ChangeByOxygenBPS.__init__(self, bacterium_metabolism_from, bacterium_metabolism_to, probability, oxygen_high)
