__author__ = "Michael J. Pitcher"

from ..Base.MetapopulationNetwork import *
from BronchopulmonarySegment import *
from LymphNode import *
from PulmonaryAnatomyClasses import *

import matplotlib.pyplot as plt


class LungLymphNetwork(MetapopulationNetwork):

    def __init__(self, population_keys, events, bps_positions=None, ln_positions=None, bronchi=None,
                 lymphatic_vessels=None, weight_method=HORSFIELD):

        if bps_positions is None:
            bps_positions = get_default_bps_positions()
        if ln_positions is None:
            ln_positions = get_default_ln_positions()
        if bronchi is None:
            bronchi = get_default_bronchi()
        if lymphatic_vessels is None:
            lymphatic_vessels = get_default_lymphatic_vessels()

        self.node_list_bps = []
        self.node_list_ln = []
        bps_ids = range(0, 36)
        ln_ids = range(36, 45)

        nodes = []

        # BPS nodes
        for id in bps_ids:
            bps_node = BronchopulmonarySegment(id, population_keys, bps_positions[id])
            nodes.append(bps_node)
            self.node_list_bps.append(bps_node)

        # Lymph nodes
        for id in ln_ids:
            ln_node = LymphNode(id, population_keys, ln_positions[id])
            nodes.append(ln_node)
            self.node_list_ln.append(ln_node)

        edges = []

        # Bronchus edges
        for (node1_id, node2_id) in bronchi:
            node1 = [n for n in nodes if n.id == node1_id][0]
            node2 = [n for n in nodes if n.id == node2_id][0]
            edge_data = {EDGE_TYPE: BRONCHUS, WEIGHT: 0}
            bronchus_edge = (node1, node2, edge_data)
            edges.append(bronchus_edge)

        # Lymphatic edges
        for (node1_id, node2_id) in lymphatic_vessels:
            node1 = [n for n in nodes if n.id == node1_id][0]
            node2 = [n for n in nodes if n.id == node2_id][0]
            edge_data = {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: node2}
            lymphatic_edge = (node1, node2, edge_data)
            edges.append(lymphatic_edge)

        MetapopulationNetwork.__init__(self, population_keys, nodes, edges, events)

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
                            edge_data[EDGE_TYPE] == BRONCHUS and edge_data[WEIGHT] == 0.0]

            assert len(parent_nodes) == 1
            # Get the data from parent edge to update
            parent_node = parent_nodes[0]
            # If the node is terminal, weight is 1.0
            if node.id in range(18, 36):
                self.edge[node][parent_node][WEIGHT] = 1.0
            else:
                # Get the child edges (those with weights already set) (only get bronchi)
                child_edges_weights = [edge_data[WEIGHT] for _, _, edge_data in self.edges(node, data=True) if
                                       edge_data[EDGE_TYPE] == BRONCHUS and edge_data[WEIGHT] > 0.0]

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

    def display(self, node_contents_species, title="", save_name=None, show_edge_labels=False):
        fig = plt.figure(figsize=(10, 10))
        plt.axis('off')
        plt.title(title)

        pos = {}
        node_labels = {}
        for n in self.nodes():
            pos[n] = n.position
            node_labels[n] = ""
            if node_contents_species is not None:
                for species in node_contents_species:
                    node_labels[n] += str(n.subpopulations[species]) + ":"

        # Nodes
        nx.draw_networkx_nodes(self, nodelist=self.node_list_bps, pos=pos, node_size=500, node_color="red")
        nx.draw_networkx_nodes(self, nodelist=self.node_list_ln, pos=pos, node_size=200, node_color="grey",
                               node_shape='p')

        # Node labels
        nx.draw_networkx_labels(self, pos, labels=node_labels, font_family='sans-serif')
        # Edges

        bronchi_edges = [(e1, e2) for (e1, e2, data) in self.edges(data=True) if data[EDGE_TYPE] == BRONCHUS]
        edge_widths = [data[WEIGHT] * 2 for (_, _, data) in self.edges(data=True) if
                       data[EDGE_TYPE] == BRONCHUS]
        nx.draw_networkx_edges(self, pos, edgelist=bronchi_edges, edge_color='red', width=edge_widths)
        lymphatic_vessels = [(e1, e2) for (e1, e2, data) in self.edges(data=True) if data[EDGE_TYPE] ==
                             LYMPHATIC_VESSEL]
        nx.draw_networkx_edges(self, pos, edgelist=lymphatic_vessels, edge_color='grey', width=5)

        plt.show()
        if save_name is not None:
            fig.savefig(save_name + ".png")  # save as png

    def get_neighbouring_edges(self, node, edge_type=None):
        # TODO - may be slow to calculate this all the time, better to do it once and save
        if edge_type is None:
            neighbouring_edges = [(neighbour, data) for (_, neighbour, data) in self.edges(node, data=True)]
        elif edge_type == BRONCHUS:
            neighbouring_edges = [(neighbour, data) for (_, neighbour, data) in self.edges(node, data=True)
                                  if data[EDGE_TYPE] == BRONCHUS]
        elif edge_type == LYMPHATIC_VESSEL:
            neighbouring_edges = [(neighbour, data) for (_, neighbour, data) in self.edges(node, data=True)
                                  if data[EDGE_TYPE] == LYMPHATIC_VESSEL and data[DIRECTION] != node]
        else:
            raise Exception("Incorrect edge type: {0}".format(edge_type))
        return neighbouring_edges

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