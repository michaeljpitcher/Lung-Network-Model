#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Base.Events.Phagocytosis import Phagocytosis
from ..Events.BacteriaReplication import BacteriaReplication
from ..TBClasses import *
from ...Pulmonary.Network.PulmonaryAnatomyNetwork import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TBModelBasic(PulmonaryAnatomyNetwork):

    def __init__(self, seeding, probabity_bac_rep, probability_mac_ingest):

        compartments = [BACTERIA, MACROPHAGE]
        events_and_node_types = dict()

        bac_rep = BacteriaReplication(probabity_bac_rep, BACTERIA)
        mac_ingest_bac = Phagocytosis(probability_mac_ingest, MACROPHAGE, BACTERIA)

        events_and_node_types[bac_rep] = [BronchopulmonarySegment, BronchialTreeNode]
        events_and_node_types[mac_ingest_bac] = [BronchopulmonarySegment, BronchialTreeNode]

        PulmonaryAnatomyNetwork.__init__(self, compartments, events_and_node_types, bronchial_tree_nodes=True,
                                         lymphatic_nodes=False, haematogenous_reseeding=False)

        self.seed_network(seeding)
