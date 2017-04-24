#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Base.Events.Destruction import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Phagocytosis(Destroy):

    def __init__(self, node_types, probability, phagocyte_compartment, compartment_to_ingest,
                 compartment_to_change_phagocyte_to=None, compartment_to_change_ingested_to=None):
        self.phagocyte_compartment = phagocyte_compartment
        self.compartment_to_change_phagocyte_to = compartment_to_change_phagocyte_to
        self.compartment_to_change_ingested_to = compartment_to_change_ingested_to
        Destroy.__init__(self, node_types, probability, compartment_to_ingest)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.phagocyte_compartment] * Destroy.increment_from_node(self, node, network)

    def update_node(self, node, network):
        if self.compartment_to_change_phagocyte_to:
            node.update_subpopulation(self.phagocyte_compartment, -1)
            node.update_subpopulation(self.compartment_to_change_phagocyte_to, 1)

        Destroy.update_node(self, node, network)

        if self.compartment_to_change_ingested_to:
            node.update_subpopulation(self.compartment_to_change_ingested_to, 1)


class PhagocyteDestroyInternals(Destroy):
    # TODO - check whether this should be destruction of everything, dependent on load

    def __init__(self, node_types, probability, phagocyte_compartment, bacteria_compartment,
                 healed_phagocyte_compartment):
        self.phagocyte_compartment = phagocyte_compartment
        # Compartment to return macrophage to if it destroys its last bacteria
        self.healed_phagocyte_compartment = healed_phagocyte_compartment
        Destroy.__init__(self, node_types, probability, bacteria_compartment)

    def increment_from_node(self, node, network):
        # If there are intracellular bacteria present, then based on number of macs, else no chance
        if node.subpopulations[self.compartment_destroyed] > 0:
            return node.subpopulations[self.phagocyte_compartment]
        else:
            return 0

    def update_node(self, node, network):
        Destroy.update_node(self, node, network)
        if node.subpopulations[self.compartment_destroyed] < node.subpopulations[self.phagocyte_compartment]:
            node.update_subpopulation(self.phagocyte_compartment, -1)
            node.update_subpopulation(self.healed_phagocyte_compartment, 1)
