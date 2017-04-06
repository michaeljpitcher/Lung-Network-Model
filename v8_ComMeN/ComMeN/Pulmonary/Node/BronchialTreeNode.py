#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Base.Node.Patch import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class BronchialTreeNode(Patch):

    def __init__(self, compartments, ventilation, perfusion, position):
        Patch.__init__(compartments, position)
        self.ventilation = ventilation
        self.perfusion = perfusion
        self.oxygen_tension = self.ventilation / self.perfusion
