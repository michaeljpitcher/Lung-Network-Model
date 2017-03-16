__author__ = "Michael J. Pitcher"

from LungNetwork import *
from LymphNode import *


class LungLymphMetapopulationNetwork(LungMetapopulationNetwork):

    def __init__(self, population_keys, events, bps_positions=None, bronchi_definitions=None, ln_positions=None,
                 lymphatic_vessels_definitions=None, weight_method=HORSFIELD):
        """

        :param population_keys:
        :param events:
        :param bps_positions:
        :param bronchi_definitions:
        :param ln_positions:
        :param lymphatic_vessels_definitions:
        :param weight_method:
        """

        # Call Lung network to create network, then add lymph nodes, edges on top
        LungMetapopulationNetwork.__init__(self, population_keys, events, bps_positions, bronchi_definitions,
                                           weight_method=weight_method)

        # Positions
        if not ln_positions:
            ln_positions = get_default_ln_positions()

        # Edges
        if not lymphatic_vessels_definitions:
            lymphatic_vessels_definitions = get_default_lymphatic_vessels()

        # ID list
        ln_ids = range(36, 45)
        # Node list
        self.node_list_ln = []
        # Add Lymph Nodes
        for id in ln_ids:
            # If it's a terminal node, set value on the Node
            if id == 44 or id == 41:
                ln_node = LymphNode(id, population_keys, ln_positions[id], terminal=True)
            else:
                ln_node = LymphNode(id, population_keys, ln_positions[id])
            self.add_node(ln_node)
            self.node_list_ln.append(ln_node)

        # Add Lymphatic edges
        for (node1_id, node2_id) in lymphatic_vessels_definitions:
            node1 = [n for n in self.nodes() if n.id == node1_id][0]
            node2 = [n for n in self.nodes() if n.id == node2_id][0]
            edge_data = {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: node2}
            self.add_edge(node1, node2, edge_data)

    def display_network(self, class_types_to_display, title="", save_name=None):
        """
        Output the network
        :param class_types_to_display:
        :param title:
        :param save_name:
        :return:
        """

        node_colours = {BronchopulmonarySegment: 'green', LymphNode: 'grey'}
        edge_colours = {BRONCHUS: 'green', LYMPHATIC_VESSEL: 'grey'}
        MetapopulationNetwork.display(self, class_types_to_display, node_colours, edge_colours, title, save_name)


# STATIC METHODS
def get_default_ln_positions():
    ln_positions = dict()
    ln_positions[36] = (6, 4.6)
    ln_positions[37] = (4.5, 5.1)
    ln_positions[38] = (5, 5.9)
    ln_positions[39] = (4.25, 6.1)
    ln_positions[40] = (4.5, 7.6)
    ln_positions[41] = (4.21, 9.75)
    ln_positions[42] = (5.9, 7.05)
    ln_positions[43] = (5.8, 8.2)
    ln_positions[44] = (6.0, 9.8)
    return ln_positions


def get_default_lymphatic_vessels():
    lymphatic_vessels = [(36, 38), (37, 38), (38, 40), (39, 40), (40, 41), (42, 43), (43, 44)]
    for drainage_id in range(32, 36):
        lymphatic_vessels.append((drainage_id, 36))
    for drainage_id in range(28, 32):
        lymphatic_vessels.append((drainage_id, 42))
    for drainage_id in range(23, 28):
        lymphatic_vessels.append((drainage_id, 37))
    for drainage_id in range(18, 23):
        lymphatic_vessels.append((drainage_id, 39))
    return lymphatic_vessels


