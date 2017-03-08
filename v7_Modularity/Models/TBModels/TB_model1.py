__author__ = "Michael J. Pitcher"

from ..Lung.LungLymphNetwork import *
from ..TBEvents import *

class TBModel1(LungLymphNetwork):

    def __init__(self, species, loads, positions, events, weight_method=HORSFIELD):

        LungLymphNetwork.__init__(self, species, loads, positions, events, weight_method)
