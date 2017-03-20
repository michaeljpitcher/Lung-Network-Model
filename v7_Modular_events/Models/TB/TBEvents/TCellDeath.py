__author__ = "Michael J. Pitcher"

from ...Base.Events.Die import *


class TCellDeath(Die):

    def __init__(self, t_cell_type, probability):
        Die.__init__(self, t_cell_type, probability)
