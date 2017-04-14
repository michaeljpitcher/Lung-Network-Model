#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Destruction import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TCellDeathRegular(Destroy):

    def __init__(self, node_types, probability, t_cell_compartment):
        Destroy.__init__(self, node_types, probability, t_cell_compartment)
