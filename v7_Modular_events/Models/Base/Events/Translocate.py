__author__ = "Michael J. Pitcher"

from Event import *


class Translocate(Event):

    def __init__(self, class_translocating, edge_type, probability):
        self.class_translocating = class_translocating
        self.edge_type = edge_type
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_translocating]

    def update_network(self, chosen_node, network):
        (neighbour, edge_data) = self.pick_an_edge(chosen_node, network)
        chosen_node.update(self.class_translocating, -1)
        neighbour.update(self.class_translocating, 1)

    def pick_an_edge(self, chosen_node, network):
        # Pick edge at random from those available
        edges = network.get_neighbouring_edges(chosen_node, self.edge_type)
        index = np.random.randint(0, len(edges))
        return edges[index]


class TranslocateByDegree(Translocate):

    def __init__(self, class_translocating, edge_type, probability):
        Translocate.__init__(self, class_translocating, edge_type, probability)

    def increment_from_node(self, node, network):
        if self.edge_type in node.degrees:
            return node.subpopulations[self.class_translocating] * node.degrees[self.edge_type]
        else:
            return 0