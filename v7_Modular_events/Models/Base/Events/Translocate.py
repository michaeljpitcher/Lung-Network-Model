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
        edges = network.get_neighbouring_edges(chosen_node, self.edge_type)
        neighbour = self.pick_a_neighbour(edges)
        amounts_to_move = self.amounts_to_move(chosen_node)
        for key in amounts_to_move:
            chosen_node.update(key, -1 * amounts_to_move[key])
            neighbour.update(key, amounts_to_move[key])

    def pick_a_neighbour(self, edges):
        # Pick edge at random from those available
        neighbour, data = edges[np.random.randint(0, len(edges))]
        return neighbour

    def amounts_to_move(self, node):
        return {self.class_translocating: 1}


class TranslocateByDegree(Translocate):

    def __init__(self, class_translocating, edge_type, probability):
        Translocate.__init__(self, class_translocating, edge_type, probability)

    def increment_from_node(self, node, network):
        if self.edge_type in node.degrees:
            return node.subpopulations[self.class_translocating] * node.degrees[self.edge_type]
        else:
            return 0