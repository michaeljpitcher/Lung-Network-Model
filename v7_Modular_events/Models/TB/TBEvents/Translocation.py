__author__ = "Michael J. Pitcher"

from ...Base.Event import *
from ...PulmonaryAnatomy.PulmonaryAnatomyClasses import *
from ..TBClasses import *


class Translocation(Event):

    def __init__(self, class_type, edge_type, probability):
        self.class_type = class_type
        self.edge_type = edge_type
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_type] * len(network.get_neighbouring_edges(node, self.edge_type))

    def update_network(self, chosen_node, network):
        neighbours = network.get_neighbouring_edges(chosen_node, self.edge_type)
        chosen_neighbour = None

        if self.edge_type == BRONCHUS:
            total_weight = sum(edge_data[WEIGHT] for (neighbour, edge_data) in neighbours)
            r = np.random.random() * total_weight
            running_total = 0
            for (neighbour, edge_data) in neighbours:
                running_total += edge_data[WEIGHT]
                if running_total > r:
                    chosen_neighbour = neighbour
        elif self.edge_type == LYMPHATIC_VESSEL:
            r = np.random.randint(0, len(neighbours))
            (neighbour, edge_data) = neighbours[r]
            chosen_neighbour = neighbour
        else:
            raise Exception("Invalid edge type")

        # Neighbour has been chosen, check if bacteria need to be moved
        if self.class_type == MACROPHAGE_INFECTED:
            bacteria_to_move = int(round(chosen_node.subpopulations[BACTERIA_INTRACELLULAR] /
                                         chosen_node.subpopulations[MACROPHAGE_INFECTED]))
            chosen_node.update(BACTERIA_INTRACELLULAR, -1 * bacteria_to_move)
            chosen_neighbour.update(BACTERIA_INTRACELLULAR, bacteria_to_move)

        chosen_node.update(self.class_type, -1)
        chosen_neighbour.update(self.class_type, 1)
