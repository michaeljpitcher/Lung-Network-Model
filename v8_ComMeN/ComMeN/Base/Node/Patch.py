#!/usr/bin/env python

"""Class representing a node on a metapopulation network

Long Docstring

"""

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Patch:

    def __init__(self, node_id, compartments, position=(0, 0)):
        self.node_id = node_id
        self.subpopulations = dict()
        for compartment in compartments:
            self.subpopulations[compartment] = 0
        self.position = position
        self.neighbours = []

    def __str__(self):
        return "Patch [" + str(self.node_id) + "]"

    def update_subpopulation(self, compartment, alteration):
        assert compartment in self.subpopulations.keys(), "Invalid compartment {0} for update".format(compartment)
        self.subpopulations[compartment] += alteration
        assert self.subpopulations[compartment] >= 0, "Compartment {0} count cannot drop below 0".format(compartment)

    def compartment_per_compartment(self, compartment_a, compartment_b):
        return int(round(self.subpopulations[compartment_a] / self.subpopulations[compartment_b]))
