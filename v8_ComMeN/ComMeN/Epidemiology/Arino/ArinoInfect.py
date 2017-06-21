#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Change import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class ArinoInfect(Change):
    """
    As per change by other compartments, but based on the total population at node (mostly used for epidemiology)
    """
    def __init__(self, node_types, susceptible_compartment, compartment_to, infectious_compartments):
        self.infectious_compartments = infectious_compartments
        # Prob is 1 - will depend on the infection rate beta at the patch
        Change.__init__(self, node_types, 1, susceptible_compartment, compartment_to)

    def increment_state_variable_from_node(self, node, network):
        total_population = float(sum(node.subpopulations.values()))

        if total_population == 0:
            return 0
        else:
            total_infectious = sum([node.subpopulations[n] for n in self.infectious_compartments])
            return node.beta * (node.subpopulations[self.compartment_from] * total_infectious) / total_population
