#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from Event import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Destroy(Event):

    def __init__(self, node_types, probability, compartment_destroyed, internals_to_destroy=None,
                 internals_changed=None):
        self.compartment_destroyed = compartment_destroyed
        self.internals_to_destroy = internals_to_destroy
        if internals_changed:
            for record in internals_changed:
                assert len(record) == 2, "Must provide a compartment from and to"
        self.internals_changed = internals_changed
        Event.__init__(self, node_types, probability)

    def increment_state_variable_from_node(self, node, network):
        return node.subpopulations[self.compartment_destroyed]

    def update_node(self, node, network):
        if self.internals_to_destroy:
            destroy_internals(self.internals_to_destroy, self.compartment_destroyed, node)
        if self.internals_changed:
            for (internal_compartment, new_compartment) in self.internals_changed:
                amount = node.compartment_per_compartment(internal_compartment, self.compartment_destroyed)
                node.update_subpopulation(internal_compartment, -1 * amount)
                node.update_subpopulation(new_compartment, amount)
        node.update_subpopulation(self.compartment_destroyed, -1)


class DestroyByOtherCompartments(Destroy):
    def __init__(self, node_types, probability, compartment_destroyed, influencing_compartments,
                 internals_to_destroy=None, internals_changed=None,
                 influencers_to_destroy=None, influencers_changed=None):
        self.influencing_compartments = influencing_compartments
        self.influencers_to_destroy = influencers_to_destroy
        if influencers_changed:
            for record in influencers_changed:
                assert len(record) == 2, "Must provide a compartment from and to"
        self.influencers_changed = influencers_changed
        Destroy.__init__(self, node_types, probability, compartment_destroyed, internals_to_destroy, internals_changed)

    def increment_state_variable_from_node(self, node, network):
        return Destroy.increment_state_variable_from_node(self, node, network) * \
               sum([node.subpopulations[c] for c in self.influencing_compartments])

    def update_node(self, node, network):
        Destroy.update_node(self, node, network)
        if self.influencers_to_destroy:
            for c in self.influencers_to_destroy:
                node.update_subpopulation(c, -1)
        if self.influencers_changed:
            for (influencing_compartment, new_compartment) in self.influencers_changed:
                node.update_subpopulation(influencing_compartment, -1)
                node.update_subpopulation(new_compartment, 1)
