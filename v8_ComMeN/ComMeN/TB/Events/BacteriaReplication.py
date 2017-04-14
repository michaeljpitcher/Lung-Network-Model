#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Creation import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class BacteriaReplication(Replication):

    def __init__(self, node_types, probability, bacteria_compartment):
        Replication.__init__(self, node_types, probability, bacteria_compartment)
