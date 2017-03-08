__author__ = "Michael J. Pitcher"

from ..Base.Event import *


class BacteriaReplication(Event):

    def __init__(self, probability, metabolism):
        self.metabolism = metabolism
        Event.__init__(self, probability)

    def increment_from_node(self, node):
        return node.subpopulations[self.metabolism]

    def action(self, node, network):
        node.update(self.metabolism, 1)
