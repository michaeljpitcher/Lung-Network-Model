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


class LymphNode(LungPatch):

    def __init__(self, node_id, compartments, position, drugs=None):
        LungPatch.__init__(self, node_id, compartments, position, drugs)
