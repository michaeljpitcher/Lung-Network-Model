#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Pulmonary.Network.PulmonaryAnatomyNetwork import *
from ..Events.BacteriaChange import *
from ..Events.BacteriaReplication import *
from ..Events.BacteriaTranslocate import *
from ..Events.MacrophageActivation import *
from ..Events.MacrophageDeath import *
from ..Events.MacrophageIngestBacteria import *
from ..Events.MacrophageRecruitment import *
from ..Events.MacrophageTranslocate import *
from ..Events.TCellDeath import *
from ..Events.TCellRecruitment import *
from ..Events.TCellTranslocate import *
from ..TBClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TBModelFull(PulmonaryAnatomyNetwork):

    def __init__(self, seeding, rate_bac_rep_fast):

        compartments = [BACTERIA_FAST, BACTERIA_SLOW, BACTERIA_INTRACELLULAR] + \
                       [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED] + \
                       [T_CELL]

        events_node_types = dict()
        # Replication
        bac_rep_fast = BacteriaReplication(rate_bac_rep_fast, BACTERIA_FAST)
        events_node_types





        PulmonaryAnatomyNetwork(self.compartments)