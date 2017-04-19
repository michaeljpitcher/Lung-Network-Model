#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Pulmonary.Network.PulmonaryAnatomyNetwork import *
from ComMeN.TB.EventsWithCompartments.TCellRecruitment import *
from ComMeN.Pulmonary.Visuals.PulmonaryNetworkGraph import *


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

event = TCellRecruitmentBronchialRegular(0.1)
a = PulmonaryAnatomyNetwork(['a','b'],[event], True,HORSFIELD,True,True)

draw_pulmonary_network_graph(a, "TITLE")