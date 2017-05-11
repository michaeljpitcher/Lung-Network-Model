#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Change import *
from ..EpidemiologyClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class KeelingRecover(Change):
    def __init__(self, node_types, m_r, g_r):
        Change.__init__(self, node_types, m_r * g_r, RAT_INFECTIOUS, RAT_RESISTANT)