#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Node.Patch import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class BronchopulmonarySegment(Patch):

    def __init__(self, node_id, compartments, ventilation, perfusion, position):
        Patch.__init__(self, node_id, compartments, position)
        self.ventilation = ventilation
        self.perfusion = perfusion

        # TODO - how to calculate oxygen tension?
        if self.ventilation - self.perfusion <= 0:
            self.oxygen_tension = 0.0000000001
        else:
            self.oxygen_tension = self.ventilation - self.perfusion
