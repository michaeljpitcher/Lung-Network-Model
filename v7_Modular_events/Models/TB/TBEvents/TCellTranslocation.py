__author__ = "Michael J. Pitcher"

from ...PulmonaryAnatomy.PulmonaryEvents.PulmonaryTranslocate import *


class TCellTranslocateLymph(TranslocateLymphatic):

    def __init__(self, t_cell_type, probability):
        TranslocateLymphatic.__init__(self, t_cell_type, probability)
