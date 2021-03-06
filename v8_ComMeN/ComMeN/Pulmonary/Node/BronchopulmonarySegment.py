#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungPatch import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class BronchopulmonarySegment(LungPatch):

    def __init__(self, node_id, compartments, ventilation, perfusion, position, drugs=None):
        LungPatch.__init__(self, node_id, compartments, position, drugs)
        self.ventilation = ventilation
        self.perfusion = perfusion

        # TODO - how to calculate oxygen tension?
        if self.ventilation - self.perfusion <= 0:
            self.oxygen_tension = 0.0000000001
        else:
            self.oxygen_tension = self.ventilation - self.perfusion

    def __str__(self):
        return "BronchopulmonarySegment {" + str(self.node_id) + "}"
