__author__ = "Michael J. Pitcher"

from ...PulmonaryAnatomy.PulmonaryEvents.PulmonaryChange import *
from ..TBClasses import *


class BacteriumChangeMetabolism(ChangeByOxygenBPS):

    def __init__(self, bacterium_metabolism_from, bacterium_metabolism_to, probability):
        if bacterium_metabolism_from == BACTERIA_FAST and bacterium_metabolism_to == BACTERIA_SLOW:
            oxygen_high = False
        elif bacterium_metabolism_from == BACTERIA_SLOW and bacterium_metabolism_to == BACTERIA_FAST:
            oxygen_high = True
        else:
            raise Exception("Invalid bacteria types {0}, {1}".format(bacterium_metabolism_from,
                                                                     bacterium_metabolism_to))
        ChangeByOxygenBPS.__init__(self, bacterium_metabolism_from, bacterium_metabolism_to, probability, oxygen_high)
