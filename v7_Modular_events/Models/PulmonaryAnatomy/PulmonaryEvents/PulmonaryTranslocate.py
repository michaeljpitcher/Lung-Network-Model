__author__ = "Michael J. Pitcher"

from ...Base.Events.Translocate import *
from ..PulmonaryAnatomyClasses import *


class TranslocateBronchus(TranslocateByDegree):

    def __init__(self, type_to_translocate, probability, move_by_edge_weight=True):
        self.move_by_edge_weight = move_by_edge_weight
        TranslocateByDegree.__init__(self, type_to_translocate, BRONCHUS, probability)

    def pick_a_neighbour(self, edges):
        # Want to move based on the bronchi weights
        if self.move_by_edge_weight:
            total_weight = sum([data[WEIGHT] for (neighbour, data) in edges])
            r = np.random.random() * total_weight
            running_total = 0
            for (neighbour, data) in edges:
                running_total += data[WEIGHT]
                if running_total > r:
                    return neighbour
        else:
            # Defer to super class
            return TranslocateByDegree.pick_a_neighbour(self, edges)


class TranslocateLymphatic(TranslocateByDegree):
    def __init__(self, type_to_translocate, probability):
        TranslocateByDegree.__init__(self, type_to_translocate, LYMPHATIC_VESSEL, probability)

    def increment_from_node(self, node, network):
        viable_edges = [(neighbour, data) for (neighbour, data) in
                        network.get_neighbouring_edges(node, LYMPHATIC_VESSEL) if data[DIRECTION] == neighbour]
        return node.subpopulations[self.class_translocating] * len(viable_edges)

    def pick_a_neighbour(self, edges):
        # Reduce the edges to only those in the direction of lymph flow
        viable_edges = [(n,d) for (n,d) in edges if d[DIRECTION] == n]
        return TranslocateByDegree.pick_a_neighbour(self, viable_edges)
