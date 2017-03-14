__author__ = "Michael J. Pitcher"

from ...Base.Event import *
from ...PulmonaryAnatomy.PulmonaryAnatomyClasses import *
from ..TBClasses import *
from ...PulmonaryAnatomy.BronchopulmonarySegment import *
from ...PulmonaryAnatomy.LymphNode import *


class Translocate(Event):

    def __init__(self, class_type, edge_type, probability):
        self.class_type = class_type
        self.edge_type = edge_type
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_type] * len(network.get_neighbouring_edges(node, self.edge_type))

    def update_network(self, chosen_node, network):

        (neighbour, edge_data) = self.pick_an_edge(chosen_node, network)

        if self.class_type in CLASSES_WITH_INTRACELLULAR:
            bacteria_to_move = int(round(chosen_node.subpopulations[BACTERIA_INTRACELLULAR]) /
                                   chosen_node.subpopulations[self.class_type])
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

    def __init__(self, class_type, probability, redistribute=True):
        self.redistribute = redistribute
        Translocate.__init__(self, class_type, LYMPHATIC_VESSEL, probability)

    def increment_from_node(self, node, network):
        edges = [(neighbour, data) for (neighbour, data) in network.get_neighbouring_edges(node, LYMPHATIC_VESSEL) if
                 data[DIRECTION] != node]
        return node.subpopulations[self.class_type] * len(edges)

    def pick_an_edge(self, chosen_node, network):
        # Only pick edges which flow away from the node
        edges = [(neighbour, data) for (neighbour, data) in network.get_neighbouring_edges(chosen_node,
                LYMPHATIC_VESSEL) if data[DIRECTION] != chosen_node]

        # Should only be one TODO - this might change
        assert len(edges) == 1, "Incorrect number of lymph edges = {0}".format(len(edges))

        if self.redistribute and edges[0][0].terminal:
            # Redistribution is active and Node is terminal, so haematogenous spread
            possible_nodes = network.terminal_bps_nodes
            total_perfusion = sum(n.perfusion for n in possible_nodes)
            r = np.random.random() * total_perfusion
            running_total = 0
            for n in possible_nodes:
                running_total += n.perfusion
                if running_total > r:
                    return n, None
        else:
            return edges[0]


class TranslocateLymphToBPS(Translocate):
    """
    Transfer from a lymph node to a BPS (with option to base redistribution by infection level)
    """

    def __init__(self, class_type, probability, based_on_infection=False):
        self.based_on_infection = based_on_infection
        Translocate.__init__(self, class_type, LYMPHATIC_VESSEL, probability)

    def increment_from_node(self, node, network):
        if isinstance(node, LymphNode):
            edges = [(n, d) for (n, d) in network.get_neighbouring_edges(node, LYMPHATIC_VESSEL) if
                     isinstance(n, BronchopulmonarySegment)]
            return node.subpopulations[self.class_type] * len(edges)
        else:
            return 0

    def pick_an_edge(self, chosen_node, network):

        edges = [(neighbour, data) for (neighbour, data) in network.get_neighbouring_edges(chosen_node,
                    LYMPHATIC_VESSEL) if isinstance(neighbour, BronchopulmonarySegment)]
        if self.based_on_infection:
            total_infection = sum([n.subpopulations[MACROPHAGE_INFECTED] for (n, d) in edges])
            r = np.random.random() * total_infection
            running_total = 0
            for (neighbour, data) in edges:
                running_total += neighbour.subpopulations[MACROPHAGE_INFECTED]
                if running_total > r:
                    return neighbour, data
        else:
            index = np.random.randint(0, len(edges))
            return edges[index]
