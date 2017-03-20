__author__ = "Michael J. Pitcher"

from Event import *


class Create(Event):

    def __init__(self, class_to_create, probability):
        self.class_to_create = class_to_create
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        # Spontaneous appearance
        return 1

    def update_network(self, chosen_node, network):
        chosen_node.update(self.class_to_create, 1)


class CreateAtNodeType(Create):

    def __init__(self, class_to_create, node_type, probability):
        self.node_type = node_type
        Create.__init__(self, class_to_create, probability)

    def increment_from_node(self, node, network):
        if isinstance(node, self.class_to_create):
            return Create.increment_from_node(self, node, network)
        else:
            return 0


class Replication(Create):
    """ An individual is create by a member of it's class replicating (splitting in two)
    """

    def __init__(self, class_to_create, probability):
        Create.__init__(self, class_to_create, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_to_create]