from ..Base.MetapopulationNetwork import *
from .BronchopulmonarySegment import BronchopulmonarySegment
from .LymphNode import LymphNode

BPS_POSITIONS = "BronchopulmonarySegmentPositions"
LN_POSITIONS = "LymphNodePositions"
BRONCHUS = "bronchus"
WEIGHT = "weight"
LYMPHATIC_VESSEL = "lymphatic_vessel"
DIRECTION = "direction"
HORSFIELD = "horsfield"
STAHLER = "stahler"


class LungLymphNetwork(MetapopulationNetwork):

    def __init__(self, species, loads, positions, events, weight_method=HORSFIELD):

        bps_ids = range(0, 36)
        terminal_bps_ids = range(18, 36)
        ln_ids = range(36, 45)

        # -----------START NODES ---------------------------
        self.node_list_bps = []
        self.node_list_ln = []
        self.node_list_terminal_bps = []

        nodes = []

        # BPSs
        for bps_id in bps_ids:
            assert bps_id in positions.keys(), "Node {0} position has not been specified".format(bps_id)
            position = positions[bps_id]
            if bps_id in loads:
                load_for_bps = loads[bps_id]
            else:
                load_for_bps = {}
            node = BronchopulmonarySegment(bps_id, species, load_for_bps, position)
            nodes.append(node)
            self.node_list_bps.append(node)
            if bps_id in terminal_bps_ids:
                self.node_list_terminal_bps.append(node)

        # Lymph nodes
        for ln_id in ln_ids:
            assert ln_id in positions.keys(), "Node {0} position has not been specified".format(ln_id)
            position = positions[ln_id]
            if ln_id in loads:
                load_for_bps = loads[ln_id]
            else:
                load_for_bps = {}
            node = LymphNode(ln_id, species, load_for_bps, position)
            nodes.append(node)
            self.node_list_ln.append(node)
        # -------------END NODES ---------------------------

        # -----------START EDGES ---------------------------
        edges = []
        # Bronchi

        # List of edges - names give rough approximation of which parts of anatomy are represented
        # Trachea
        bronchi = [(0, 1)]
        # Main bronchi
        bronchi += [(1, 2), (2, 3), (1, 4)]
        # Lobar bronchi
        bronchi += [(2, 5), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10), (10, 11), (4, 12), (12, 13), (12, 14), (4, 15),
                    (15, 16), (16, 17)]
        # Segmental bronchi
        bronchi += [(5, 18), (6, 19), (6, 20), (7, 21), (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27),
                    (13, 28), (13, 29), (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]

        for (node1_index, node2_index) in bronchi:
            node1 = nodes[node1_index]
            parent_nodes = nodes[node2_index]
            edge_data = {EDGE_TYPE: BRONCHUS, WEIGHT: 0}
            edges.append((node1, parent_nodes, edge_data))

        # Lymphatic vessels
        # Between lymph nodes
        lymph_vessels = [(36, 38), (37, 38), (38, 40), (39, 40), (40, 41), (42, 43), (43, 44)]

        # Drainage
        for drainage_id in range(32, 36):
            lymph_vessels.append((drainage_id, 36))
        for drainage_id in range(28, 32):
            lymph_vessels.append((drainage_id, 42))
        for drainage_id in range(23, 28):
            lymph_vessels.append((drainage_id, 37))
        for drainage_id in range(18, 23):
            lymph_vessels.append((drainage_id, 39))

        for (node1_index, node2_index) in lymph_vessels:
            node1 = nodes[node1_index]
            parent_nodes = nodes[node2_index]
            edge_data = {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: nodes[node2_index]}
            edges.append((node1, parent_nodes, edge_data))

        # -------------END EDGES ---------------------------

        MetapopulationNetwork.__init__(self, nodes, edges, species, events)

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
            if node in self.node_list_terminal_bps:
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
        edge_widths = [data[WEIGHT]*2 for (_, _, data) in self.edges(data=True) if data[EDGE_TYPE] == BRONCHUS]
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

