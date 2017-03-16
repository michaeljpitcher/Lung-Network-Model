__author__ = "Michael J. Pitcher"

from ..Base.MetapopulationNetwork import *
from BronchopulmonarySegment import *
from PulmonaryAnatomyClasses import *


class LungMetapopulationNetwork(MetapopulationNetwork):

    def __init__(self, population_keys, events, bps_positions=None, bronchi_definitions=None, weight_method=HORSFIELD):
        """

        :param population_keys:
        :param events:
        :param bps_positions:
        :param bronchi_definitions:
        :param weight_method:
        """

        # Use defaults if no positions are specified
        if not bps_positions:
            bps_positions = get_default_bps_positions()
        if not bronchi_definitions:
            bronchi_definitions = get_default_bronchi()

        # List for quicker processing
        self.node_list_bps = []
        self.terminal_bps_nodes = []

        bps_ids = range(0, 36)
        terminal_bps_ids = range(18, 36)

        # If no additional nodes supplied, start as empty list
        nodes = []

        # BPS nodes
        for id in bps_ids:
            bps_node = BronchopulmonarySegment(id, population_keys, bps_positions[id])
            nodes.append(bps_node)
            self.node_list_bps.append(bps_node)
            # If it's an end node add to list
            if id in terminal_bps_ids:
                self.terminal_bps_nodes.append(bps_node)

        edges = []

        # Bronchus edges
        for (node1_id, node2_id) in bronchi_definitions:
            node1 = [n for n in nodes if n.id == node1_id][0]
            node2 = [n for n in nodes if n.id == node2_id][0]
            edge_data = {EDGE_TYPE: BRONCHUS, WEIGHT: 0}
            bronchus_edge = (node1, node2, edge_data)
            edges.append(bronchus_edge)

        MetapopulationNetwork.__init__(self, population_keys, events, nodes=nodes, edges=edges)

        # -------------EDGE WEIGHTS ---------------------------
        self.origin = 0

        queued_nodes = [self.node_list[self.origin]]
        ordered_nodes = []

        # Pull a node from queued nodes, add it to the start of ordered nodes and add its neighbours to queued nodes
        while len(queued_nodes) > 0:
            # Remove the first node of the queued list
            node = queued_nodes.pop()
            # Insert the new node at the start
            ordered_nodes.insert(0, node)
            # Queue up the neighbours (that aren't already ordered) of this node
            queued_nodes += [neighbour for neighbour in self.neighbors(node) if neighbour not in ordered_nodes and
                             isinstance(neighbour, BronchopulmonarySegment)]

        # Process all nodes from ordered list
        while len(ordered_nodes) > 0:
            # Pull the node from the list
            node = ordered_nodes.pop(0)
            # Don't process origin - have reached the end
            if node.id == self.origin:
                break
            # Find the parent edge (should only be one) as edge where weight hasn't already been set
            # (only check bronchi)
            parent_nodes = [parent_nodes for _, parent_nodes, edge_data in self.edges(node, data=True) if
                            edge_data[WEIGHT] == 0.0]

            assert len(parent_nodes) == 1
            # Get the data from parent edge to update
            parent_node = parent_nodes[0]
            # If the node is terminal, weight is 1.0
            if node.id in range(18, 36):
                self.edge[node][parent_node][WEIGHT] = 1.0
            else:
                # Get the child edges (those with weights already set) (only get bronchi)
                child_edges_weights = [edge_data[WEIGHT] for _, _, edge_data in self.edges(node, data=True) if
                                       edge_data[WEIGHT] > 0.0]

                # Determine new weight based on method chosen
                if weight_method == HORSFIELD:
                    # Use maximum weight + 1
                    new_order = max(child_edges_weights) + 1.0
                elif weight_method == STAHLER:
                    # If all weights are same, increment by 1, else use the max
                    if len(set(child_edges_weights)) <= 1:
                        new_order = max(child_edges_weights) + 1.0
                    else:
                        new_order = max(child_edges_weights)
                else:
                    raise Exception("Invalid ordering method: {0}".format(weight_method))
                # Set the parent weight
                self.edge[node][parent_node][WEIGHT] = new_order

    def display_network(self, class_types_to_display, title="", save_name=None):
        """

        :param class_types_to_display:
        :param title:
        :param save_name:
        :return:
        """
        node_colours = {BronchopulmonarySegment: 'green'}
        edge_colours = {BRONCHUS: 'green'}
        MetapopulationNetwork.display(self, class_types_to_display, node_colours, edge_colours, title, save_name)


# STATIC METHODS FOR DEFAULT POSITIONS ETC.
def get_default_bps_positions():
    bps_positions = dict()
    bps_positions[0] = (5, 10)
    bps_positions[1] = (5, 8)
    bps_positions[2] = (4, 7)
    bps_positions[3] = (3.5, 5)
    bps_positions[4] = (6, 6)
    bps_positions[5] = (3, 8)
    bps_positions[6] = (2.75, 8.5)
    bps_positions[7] = (2.5, 5)
    bps_positions[8] = (4, 4)
    bps_positions[9] = (3.5, 3)
    bps_positions[10] = (3, 2.5)
    bps_positions[11] = (2.5, 2)
    bps_positions[12] = (7, 7)
    bps_positions[13] = (7.5, 8)
    bps_positions[14] = (8, 7)
    bps_positions[15] = (6.5, 5)
    bps_positions[16] = (7.5, 4)
    bps_positions[17] = (8, 3.5)
    bps_positions[18] = (2.5, 7.5)
    bps_positions[19] = (2.5, 9)
    bps_positions[20] = (3, 9)
    bps_positions[21] = (2, 5.5)
    bps_positions[22] = (2, 4)
    bps_positions[23] = (3.5, 4.25)
    bps_positions[24] = (4, 2)
    bps_positions[25] = (2.5, 3.25)
    bps_positions[26] = (1.5, 1)
    bps_positions[27] = (2.75, 1)
    bps_positions[28] = (7.25, 8.5)
    bps_positions[29] = (8, 8.5)
    bps_positions[30] = (8.5, 7.5)
    bps_positions[31] = (8.5, 6.5)
    bps_positions[32] = (7, 5.5)
    bps_positions[33] = (7.5, 3)
    bps_positions[34] = (8.5, 4.25)
    bps_positions[35] = (8.5, 3)
    return bps_positions


def get_default_bronchi():
    bronchi = [(0, 1)]
    # Main bronchi
    bronchi += [(1, 2), (2, 3), (1, 4)]
    # Lobar bronchi
    bronchi += [(2, 5), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10), (10, 11), (4, 12), (12, 13), (12, 14), (4, 15),
                (15, 16), (16, 17)]
    # Segmental bronchi
    bronchi += [(5, 18), (6, 19), (6, 20), (7, 21), (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27),
                (13, 28), (13, 29), (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]
    return bronchi
