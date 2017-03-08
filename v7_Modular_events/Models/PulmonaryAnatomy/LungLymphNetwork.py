__author__ = "Michael J. Pitcher"

from ..Base.MetapopulationNetwork import *


class LungLymphNetwork(MetapopulationNetwork):

    def __init__(self, population_keys, events):

        nodes = []

        edges = []

        MetapopulationNetwork.__init__(self, population_keys, nodes, edges, events)