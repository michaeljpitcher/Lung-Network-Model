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


class LungLobe(Patch):
    def __init__(self, node_id, compartments, position):
        Patch.__init__(self, node_id, compartments, position)