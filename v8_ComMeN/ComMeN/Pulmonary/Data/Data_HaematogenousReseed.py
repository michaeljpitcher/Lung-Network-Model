#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from Data_BronchialTree import BRONCHOPULMONARY_SEGMENT_IDS

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

HAEMATOGENOUS_EDGES = []

for i in BRONCHOPULMONARY_SEGMENT_IDS:
    HAEMATOGENOUS_EDGES.append((41, i))
    HAEMATOGENOUS_EDGES.append((44, i))
