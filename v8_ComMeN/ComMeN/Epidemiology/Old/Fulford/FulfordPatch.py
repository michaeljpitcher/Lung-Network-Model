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


class FulfordPatch(Patch):
    def __init__(self, node_id, compartments, area, birth_rate, death_rate_juvenile, death_rate_mature):
        self.area = area
        self.birth_rate = birth_rate
        self.death_rate_juvenile = death_rate_juvenile
        self.death_rate_mature = death_rate_mature
        Patch.__init__(self, node_id, compartments)
