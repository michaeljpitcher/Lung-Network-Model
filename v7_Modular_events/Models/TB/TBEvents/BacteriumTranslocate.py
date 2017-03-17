__author__ = "Michael J. Pitcher"

from ...PulmonaryAnatomy.PulmonaryEvents.PulmonaryTranslocate import *


class BacteriumTranslocateBronchus(TranslocateBronchus):

    def __init__(self, bacterium_to_translocate, probability, move_by_edge_weight=True):
        TranslocateBronchus.__init__(self, bacterium_to_translocate,probability, move_by_edge_weight)


class BacteriumTranslocateLymphatic(TranslocateLymphatic):
    def __init__(self, bacterium_to_translocate, probability):
        TranslocateLymphatic.__init__(self, bacterium_to_translocate, probability)
