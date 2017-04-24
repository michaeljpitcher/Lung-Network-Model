#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Base.Events.Destruction import *
from v8_ComMeN.ComMeN.Base.Events.Change import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class PhagocyteDeath(Destroy):

    def __init__(self, node_types, probability, phagocyte_compartment, internal_bacteria_compartment=None,
                 bacteria_release_compartment_to=None):
        if bacteria_release_compartment_to is not None:
            assert internal_bacteria_compartment is not None, \
                "Cannot release bacteria without providing a compartment for them to be released from"
        self.internal_bacteria_compartment = internal_bacteria_compartment
        self.bacteria_release_compartment_to = bacteria_release_compartment_to
        Destroy.__init__(self, node_types, probability, phagocyte_compartment)

    def update_node(self, node, network):
        # Check if there is bacteria inside
        if self.internal_bacteria_compartment is not None:
            bac_inside_mac = node.compartment_per_compartment(self.internal_bacteria_compartment,
                                                              self.compartment_destroyed)
            node.update_subpopulation(self.internal_bacteria_compartment, -1 * bac_inside_mac)
            # Check if bacteria are released
            if self.bacteria_release_compartment_to:
                node.update_subpopulation(self.bacteria_release_compartment_to, bac_inside_mac)
        Destroy.update_node(self, node, network)


class PhagocyteDeathByOtherCompartments(PhagocyteDeath):

    def __init__(self, node_types, probability, phagocyte_compartment, death_causing_compartments,
                 extra_compartments_to_destroy=None, internal_bacteria_compartment=None,
                 bacteria_release_compartment_to=None):
        self.death_causing_compartments = death_causing_compartments
        self.extra_compartments_to_destroy = extra_compartments_to_destroy
        PhagocyteDeath.__init__(self, node_types, probability, phagocyte_compartment, internal_bacteria_compartment,
                                bacteria_release_compartment_to)

    def increment_from_node(self, node, network):
        return PhagocyteDeath.increment_from_node(self, node, network) * sum([node.subpopulations[c] for c in
                                                                              self.death_causing_compartments])

    def update_node(self, node, network):
        PhagocyteDeath.update_node(self, node, network)
        if self.extra_compartments_to_destroy:
            for c in self.extra_compartments_to_destroy:
                node.update_subpopulation(c, -1)
