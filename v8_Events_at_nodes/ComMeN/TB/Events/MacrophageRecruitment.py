#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Event import *
from ..TBClasses import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MacrophageRecruitmentBronchial(Event):
    def __init__(self, probability, macrophage_compartment, based_on_perfusion=True):
        self.compartment_recruited = macrophage_compartment
        self.based_on_perfusion = based_on_perfusion
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        if self.based_on_perfusion:
            return node.perfusion
        else:
            return 1

    def update_node(self, node, network):
        node.update_subpopulations(self.compartment_recruited, 1)


class MacrophageRecruitmentBronchialByInfection(Event):
    def __init__(self, probability, macrophage_recruited_compartment, infection_compartments, based_on_perfusion=True, ):
        self.compartment_recruited = macrophage_recruited_compartment
        self.based_on_perfusion = based_on_perfusion
        self.infection_compartments = infection_compartments
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        if self.based_on_perfusion:
            return node.perfusion * sum([node.subpopulations[c] for c in self.infection_compartments])
        else:
            return 1 * sum([node.subpopulations[c] for c in self.infection_compartments])

    def update_node(self, node, network):
        node.update_subpopulations(self.compartment_recruited, 1)


class MacrophageRecruitmentLymph(Event):
    def __init__(self, probability, macrophage_compartment):
        self.compartment_recruited = macrophage_compartment
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return 1

    def update_node(self, node, network):
        node.update_subpopulations(self.compartment_recruited, 1)


class MacrophageRecruitmentLymphByInfection(Event):
    def __init__(self, probability, macrophage_recruited_compartment, infection_compartments):
        self.compartment_recruited = macrophage_recruited_compartment
        self.infection_compartments = infection_compartments,
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return sum([node.subpopulations[c] for c in self.infection_compartments])

    def update_node(self, node, network):
        node.update_subpopulations(self.compartment_recruited, 1)

