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


class Change(Event):
    """
    Member of one compartment spontaneously changes to a different compartment
    """

    def __init__(self, node_types, probability, compartment_from, compartment_to, internals_to_destroy=None):
        self.compartment_from = compartment_from
        self.compartment_to = compartment_to
        self.internals_to_destroy = internals_to_destroy
        Event.__init__(self, node_types, probability)

    def increment_state_variable_from_node(self, node, network):
        # Based solely on number of current population
        return node.subpopulations[self.compartment_from]

    def update_node(self, node, network):
        # Destroy any internals if needed, else change (by increasing compartment from by 1, decreasing to by 1)
        if self.internals_to_destroy:
            destroy_internals(self.internals_to_destroy, self.compartment_from, node)
        node.update_subpopulation(self.compartment_from, -1)
        node.update_subpopulation(self.compartment_to, 1)


class ChangeByOtherCompartments(Change):
    """
    Member of one compartment changes to a different compartment based on the number of members of a given list of
    influencing compartments. Influencing compartments may change
    """
    def __init__(self, node_types, probability, compartment_from, compartment_to, influencing_compartments,
                 internals_to_destroy=None, influencing_compartments_to_change=None):
        self.influencing_compartments = influencing_compartments
        self.influencing_compartments_to_change = influencing_compartments_to_change
        Change.__init__(self, node_types, probability, compartment_from, compartment_to, internals_to_destroy)

    def increment_state_variable_from_node(self, node, network):
        # Based on number of members of original compartment and influencing compartment. Not based on total population
        # (see infect event below).
        return Change.increment_state_variable_from_node(self, node, network) * \
               sum([node.subpopulations[c] for c in self.influencing_compartments])

    def update_node(self, node, network):
        # Change the original, and change any of the influencers if needed
        Change.update_node(self, node, network)
        if self.influencing_compartments_to_change:
            for (original_compartment, new_compartment) in self.influencing_compartments_to_change:
                node.update_subpopulation(original_compartment, -1)
                node.update_subpopulation(new_compartment, 1)


class Infect(Change):
    """
    As per change by other compartments, but based on the total population at node (mostly used for epidemiology)
    """
    def __init__(self, node_types, probability, susceptible_compartment, compartment_to, infectious_compartments):
        self.infectious_compartments = infectious_compartments
        Change.__init__(self, node_types, probability, susceptible_compartment, compartment_to)

    def increment_state_variable_from_node(self, node, network):
        total_population = float(sum(node.subpopulations.values()))
        if total_population == 0:
            return 0
        else:
            total_infectious = sum([node.subpopulations[n] for n in self.infectious_compartments])
            return (node.subpopulations[self.compartment_from] * total_infectious) / total_population


class ChangeByLackOfOtherCompartments(Change):
    """
    Member of one compartment changes to a different compartment based on the (lack of) a number of members of a given 
    list of influencing compartments
    """
    def __init__(self, node_types, probability, compartment_from, compartment_to, influencing_compartments,
                 internals_to_destroy=None):
        self.influencing_compartments = influencing_compartments
        Change.__init__(self, node_types, probability, compartment_from, compartment_to, internals_to_destroy)

    def increment_state_variable_from_node(self, node, network):
        # If no members of influencing class exist, state variable becomes very high. Else, calculated as original
        # compartment * 1 / sum of influencing compartments

        # TODO - check this: epsilon = low number
        epsilon = 0.00000001
        number_externals = sum([node.subpopulations[c] for c in self.influencing_compartments])
        if number_externals == 0:
            return Change.increment_state_variable_from_node(self, node, network) * (1 / epsilon)
        else:
            return Change.increment_state_variable_from_node(self, node, network) * (1 / number_externals)
