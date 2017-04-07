#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Creation import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class RecruitmentBronchial(Create):

    def __init__(self, probability, recruited_compartment, based_on_perfusion=True):
        self.based_on_perfusion = based_on_perfusion
        Create.__init__(self, probability, recruited_compartment)

    def increment_from_node(self, node, network):
        if self.based_on_perfusion:
            return node.perfusion
        else:
            return Create.increment_from_node(self, node, network)


class RecruitmentLymph(Create):
    def __init__(self, probability, recruited_compartment):
        Create.__init__(self, probability, recruited_compartment)
