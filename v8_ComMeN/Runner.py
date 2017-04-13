#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.TB.Models.TB_Model_Basic import TB_Model_Basic
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

seeding = {30:{BACTERIA: 10}}
m = TB_Model_Basic(seeding)