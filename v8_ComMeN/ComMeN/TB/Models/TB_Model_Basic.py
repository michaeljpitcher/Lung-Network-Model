#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..TBClasses import *
from ...Pulmonary.Network.PulmonaryAnatomyNetwork import *
from ..Events.BacteriaReplication import BacteriaReplication
from ..Events.MacrophageIngestBacteria import MacrophageIngestBacteria

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TB_Model_Basic(PulmonaryAnatomyNetwork):

    def __init__(self):

        compartments = [BACTERIA, MACROPHAGE]
        events_and_node_types = dict()
        events_and_node_types[BRONCHUS] = []
        bac_rep = BacteriaReplication(0.1, BACTERIA)
        events_and_node_types[BRONCHUS].append(bac_rep)
        mac_ingest_bac = MacrophageIngestBacteria(0.1, MACROPHAGE, BACTERIA)
        events_and_node_types[BRONCHUS].append(mac_ingest_bac)
        PulmonaryAnatomyNetwork.__init__(self, compartments, events_and_node_types, bronchial_tree_nodes=True,
                                         lymphatic_nodes=False, haematogenous_reseeding=False)

        # TODO: Seed? How do you know the nodes?