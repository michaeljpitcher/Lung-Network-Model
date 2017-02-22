from ..Base.MetapopulationNetwork import *
import ConfigParser
from .BronchopulmonarySegment import BronchopulmonarySegment
from .LymphNode import LymphNode

BPS_POSITIONS = "BronchopulmonarySegmentPositions"
LN_POSITIONS = "LymphNodePositions"
BRONCHUS = "bronchus"
WEIGHT = "weight"
LYMPHATIC_VESSEL = "lymphatic_vessel"

class LungLymph(MetapopulationNetwork):

    def __init__(self, species, loads, position_config_filename='node_positions.properties'):

        # Check the config file for node positions is set up
        node_pos_config = ConfigParser.RawConfigParser()
        if not node_pos_config.read(position_config_filename):
            raise IOError("Node position file ({0}) not found".format(position_config_filename))

        # -----------START NODES ---------------------------
        self.node_list_bps = []
        self.node_list_ln = []

        nodes = []

        # BPSs
        specified_nodes = [int(n) for n in node_pos_config.options(BPS_POSITIONS)]
        for i in range(36):
            assert i in specified_nodes, "Node {0} position has not been specified".format(i)
            position = tuple([float(a) for a in node_pos_config.get(BPS_POSITIONS, str(i))
                             .split(",")])
            if i in loads:
                load_for_bps = loads[i]
            else:
                load_for_bps = {}
            node = BronchopulmonarySegment(i, species, load_for_bps, position)
            nodes.append(node)
            self.node_list_bps.append(node)

        # Lymph nodes
        specified_nodes = [int(n) for n in node_pos_config.options(LN_POSITIONS)]
        for i in range(36, 45):
            assert i in specified_nodes, "Node {0} position has not been specified".format(i)
            position = tuple([float(a) for a in node_pos_config.get(LN_POSITIONS, str(i))
                             .split(",")])
            if i in loads:
                load_for_bps = loads[i]
            else:
                load_for_bps = {}
            node = LymphNode(i, species, load_for_bps, position)
            nodes.append(node)
            self.node_list_ln.append(node)
        # -------------END NODES ---------------------------

        # -----------START EDGES ---------------------------
        self.edge_list_bronchi = []
        self.edge_list_lymph = []

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
        bronchi += [(5, 18), (6, 19), (6, 20), (7, 21), (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27), (13, 28),
                  (13, 29), (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]

        for (node1_index, node2_index) in bronchi:
            node1 = nodes[node1_index]
            node2 = nodes[node2_index]
            edge_data = {EDGE_TYPE:BRONCHUS, WEIGHT:0}
            edges.append((node1, node2, edge_data))
            self.edge_list_bronchi.append((node1, node2, edge_data))

        # Lymphatic vessels
        # Between lymph nodes
        lymph_vessels = [(36,38), (37,38), (38,40), (39,40), (40,41), (42,43), (43,44)]
        for (node1_index, node2_index) in lymph_vessels:
            node1 = nodes[node1_index]
            node2 = nodes[node2_index]
            edge_data = {EDGE_TYPE:LYMPHATIC_VESSEL}
            edges.append((node1, node2, edge_data))
            self.edge_list_lymph.append((node1, node2, edge_data))

        # Drainage
        drainage = []
        for i in range(32, 36):
            drainage.append((i, 36))
        for i in range(28, 32):
            drainage.append((i, 42))
        for i in range(23, 28):
            drainage.append((i, 37))
        for i in range(18, 23):
            drainage.append((i, 39))

        for (node1_index, node2_index) in drainage:
            node1 = nodes[node1_index]
            node2 = nodes[node2_index]
            edge_data = {EDGE_TYPE:LYMPHATIC_VESSEL}
            edges.append((node1, node2, edge_data))
            self.edge_list_lymph.append((node1, node2, edge_data))

        # -------------END EDGES ---------------------------

        MetapopulationNetwork.__init__(self, nodes, edges, species)

    def display(self, node_contents_species, title="", save_name=None, show_edge_labels=False):
        fig = plt.figure(figsize=(10, 10))
        plt.axis('off')
        plt.title(title)

        pos = {}
        node_labels = {}
        for n in self.nodes():
            pos[n] = n.position

        # Nodes
        nx.draw_networkx_nodes(self, nodelist=self.node_list_bps, pos=pos, node_size=500, node_color="red")
        nx.draw_networkx_nodes(self, nodelist=self.node_list_ln, pos=pos, node_size=200, node_color="grey", node_shape='p')

        # Node labels
        nx.draw_networkx_labels(self, pos, labels=node_labels, font_family='sans-serif')
        # Edges

        bronchi_edges = [(e1, e2) for (e1, e2, data) in self.edge_list_bronchi]
        nx.draw_networkx_edges(self, pos, edgelist=bronchi_edges, edge_color='red', width=10)
        lymphatic_vessels = [(e1, e2) for (e1, e2, data) in self.edge_list_lymph]
        nx.draw_networkx_edges(self, pos, edgelist=lymphatic_vessels, edge_color='grey', width=5)

        plt.show()
        if save_name is not None:
            fig.savefig(save_name + ".png")  # save as png
