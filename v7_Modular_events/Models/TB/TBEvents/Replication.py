__author__ = "Michael J. Pitcher"

from ...Base.Event import *


class Replication(Event):

    def __init__(self, bacteria_metabolism, probability):
        self.metabolism = bacteria_metabolism
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.metabolism]

    def update_network(self, chosen_node, network):
        chosen_node.update(self.metabolism, 1)
