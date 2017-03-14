__author__ = "Michael J. Pitcher"

from ...Base.Event import *
from ...PulmonaryAnatomy.PulmonaryAnatomyClasses import *
from ..TBClasses import *


class Translocate(Event):

    def __init__(self, class_type, edge_type, probability):
        self.class_type = class_type
        self.edge_type = edge_type
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_type] * len(network.get_neighbouring_edges(node, self.edge_type))

    def update_network(self, chosen_node, network):

        (neighbour, edge_data) = self.pick_an_edge(chosen_node, network)

        if self.class_type == MACROPHAGE_INFECTED:
            bacteria_to_move = int(round(chosen_node.subpopulations[BACTERIA_INTRACELLULAR]) /
                                   chosen_node.subpopulations[MACROPHAGE_INFECTED])
            chosen_node.update(BACTERIA_INTRACELLULAR, -1 * bacteria_to_move)
            neighbour.update(BACTERIA_INTRACELLULAR, bacteria_to_move)

        chosen_node.update(self.class_type, -1)
        neighbour.update(self.class_type, 1)

    def pick_an_edge(self, chosen_node, network):
        edges = network.get_neighbouring_edges(chosen_node, self.edge_type)
        index = np.random.randint(0, len(edges))
        neighbour, edge_data = edges[index]
        return neighbour, edge_data


class TranslocateBronchusWeight(Translocate):

    def __init__(self, class_type, probability):
        Translocate.__init__(self, class_type, BRONCHUS, probability)

    def pick_an_edge(self, chosen_node, network):
        edges = network.get_neighbouring_edges(chosen_node, BRONCHUS)

        total_weight = sum([data[WEIGHT] for _, data in edges])
        r = np.random.random() * total_weight
        running_total = 0
        for (neighbour, edge_data) in edges:
            running_total += edge_data[WEIGHT]
            if running_total > r:
                return neighbour, edge_data


class TranslocateLymphDownstream(Translocate):

    def __init__(self, class_type, probability):
        Translocate.__init__(self, class_type, LYMPHATIC_VESSEL, probability)

    def pick_an_edge(self, chosen_node, network):
        # Only pick edges which flow away from the node
        edges = [(n, d) for (n, d) in network.get_neighbouring_edges(chosen_node, LYMPHATIC_VESSEL)
                 if d[DIRECTION] != chosen_node]

        # Should only be one TODO - this might change
        assert len(edges) == 1, "Incorrect number of lymph edges = {0}".format(len(edges))
        return edges[0]


class TranslocateLymphUpstream(Translocate):

    def __init__(self, class_type, probability):
        Translocate.__init__(self, class_type, LYMPHATIC_VESSEL, probability)

    def pick_an_edge(self, chosen_node, network):
        edges = [(n, d) for (n, d) in network.get_neighbouring_edges(chosen_node, LYMPHATIC_VESSEL)
                 if d[DIRECTION] == chosen_node]
        index = np.random.randint(0, len(edges))
        return edges[index]
