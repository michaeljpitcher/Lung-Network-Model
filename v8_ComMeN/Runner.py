#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.TB.Models.TB_Model_Basic import TBModelBasic
from ComMeN.TB.TBClasses import *
from ComMeN.Pulmonary.Node.LymphNode import *
from ComMeN.Base.Node.Patch import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

seeding = {30:{BACTERIA: 10, MACROPHAGE: 40}}
m = TBModelBasic(seeding, 0.6, 0.01)
m.run(10)

for n in m.nodes():
    print n.node_id, n.subpopulations