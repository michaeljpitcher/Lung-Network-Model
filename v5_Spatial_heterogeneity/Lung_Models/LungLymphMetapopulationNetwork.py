from v5_Spatial_heterogeneity.Base.MetapopulationNetwork import *
from v5_Spatial_heterogeneity.Lung_Models.BronchopulmonarySegment import BronchopulmonarySegment
from v5_Spatial_heterogeneity.Lung_Models.Bronchus import Bronchus
from v5_Spatial_heterogeneity.Lung_Models.LymphNode import LymphNode
from v5_Spatial_heterogeneity.Lung_Models.LymphaticVessel import LymphaticVessel
from v5_Spatial_heterogeneity.Lung_Models.Drainage import Drainage

HORSFIELD = 'horsfield'
STAHLER = 'stahler'
WEIGHT = 'weight'


class LungLymphMetapopulationNetwork(MetapopulationNetwork):
    """
    Metapopulation model of the lung

    TODO - explanation
    """

    def __init__(self, species_keys_bronch, initial_loads_bronch, species_key_lymph, initial_loads_lymph,
                 weight_method=HORSFIELD):

        # Node bronchopulmonary segment positions TODO: currently done by eye
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

        ventilations = dict()
        perfusions = dict()
        oxygen_tensions = dict()

        # Bronchopulmonary segment nodes
        for node_id in range(36):
            # TODO - find out specifics
            # Currently ventilation is on scale 0.2 to 0.65, perfusion 0.1 to 0.91
            # V - Ventilation - O2 reaching the alveolar tissue
            ventilations[node_id] = ((10-bps_positions[node_id][1])*0.05)+0.2
            # Q - Perfusion - blood that reaches the alveolar tissue
            perfusions[node_id] = ((10-bps_positions[node_id][1])*0.09)+0.1
            # V/Q - Ventilation Perfusion ratio
            oxygen_tensions[node_id] = ventilations[node_id] / perfusions[node_id]

        # Add bronchopulmonary nodes
        nodes = []
        id = 0
        while id < 36:
            if id in initial_loads_bronch:
                loads_for_node = initial_loads_bronch[id]
            else:
                # Empty dict
                loads_for_node = dict()
            # Create a bronchopulmonary segment instance
            node = BronchopulmonarySegment(id, species_keys_bronch, loads_for_node, bps_positions[id], ventilations[id],
                                           perfusions[id], oxygen_tensions[id])
            # Add to list
            nodes.append(node)
            id += 1

        # List of bronchial edges - names give rough approximation of which parts of anatomy are represented
        # Trachea
        bronchi_edges = [(0, 1)]
        # Main bronchi
        bronchi_edges += [(1, 2), (2, 3), (1, 4)]
        # Lobar bronchi
        bronchi_edges += [(2, 5), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10), (10, 11), (4, 12), (12, 13), (12, 14), (4, 15),
                  (15, 16), (16, 17)]
        # Segmental bronchi
        bronchi_edges += [(5, 18), (6, 19), (6, 20), (7, 21), (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27), (13, 28),
                  (13, 29), (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]
        # Set edge weights to zero to begin
        edges = {}
        for e in bronchi_edges:
            edges[e] = Bronchus()

        # Lymphatic system
        # TODO - realistic lymph node anatomy
        lymph_pos = dict()
        # Right side
        lymph_pos[36] = (4.5, 3.3)
        lymph_pos[37] = (4.5, 6.6)
        lymph_pos[38] = (4.5, 9.9)
        # Left side
        lymph_pos[39] = (5.5, 3.3)
        lymph_pos[40] = (5.5, 6.6)
        lymph_pos[41] = (5.5, 9.9)

        while id < 42:
            if id in initial_loads_lymph:
                loads_for_node = initial_loads_lymph[id]
            else:
                # Empty dict
                loads_for_node = dict()
            node = LymphNode(id, species_key_lymph, loads_for_node, lymph_pos[id])
            nodes.append(node)
            id += 1

        # Lymphatic vessels
        lymph_edges = [(36,37),(37,38),(39,40),(40,41)]
        for (e1, e2) in lymph_edges:
            edges[(e1, e2)] = LymphaticVessel()

        # Drainage
        nodes_to_drain_to_right_upper = range(18,23)
        for e in nodes_to_drain_to_right_upper:
            edges[(e, 37)] = Drainage()
        nodes_to_drain_to_right_lower = range(23, 28)
        for e in nodes_to_drain_to_right_lower:
            edges[(e, 36)] = Drainage()
        nodes_to_drain_to_left_upper = range(28, 32)
        for e in nodes_to_drain_to_left_upper:
            edges[(e, 40)] = Drainage()
        nodes_to_drain_to_left_lower = range(32, 36)
        for e in nodes_to_drain_to_left_lower:
            edges[(e, 39)] = Drainage()

        # Create the network (allows use of NetworkX functions like neighbours for calculating edge weights)
        MetapopulationNetwork.__init__(self, nodes, edges, species_keys_bronch)

        # Lists for quick referencing
        self.node_list_bps = [n for n in self.node_list.values() if isinstance(n, BronchopulmonarySegment)]
        self.node_list_lymph = [n for n in self.node_list.values() if isinstance(n, LymphNode)]

        # Record number adjacent bronchi
        for node in self.node_list_bps:
            neighbours = sorted([neighbour.id for neighbour in self.neighbors(node)])
            for neighbour_id in neighbours:
                neighbour = self.node_list[neighbour_id]
                edge = self.edge[node][neighbour]
                if isinstance(edge[EDGE_OBJECT], Bronchus):
                    node.bronchi.append((neighbour, edge[EDGE_OBJECT]))

        # Origin and terminal nodes (to compute edge weights)
        self.origin = 0
        self.alveoli = [n for n in self.node_list.values() if n.id in range(18,36)]

        # Calculate edge weights
        self.set_weights(weight_method)

    def set_weights(self, weight_method):
        """
        Set edge weights.

        Terminal branches have order 1. Other branches depend on ordering method:
        Horsfield - parent branch has order 1 greater than maximum of child branches
        Stahler - parent branch has order 1 greater than child branches if they are equal, else has max of child orders
        :return:
        """

        # Get the nodes in an ordered list - gives a list where all child nodes appear in list before parent
        # So can add the order of an edge as all child edges (those further from origin) will already have been computed
        # Start with origin node
        queued_nodes = [self.node_list[self.origin]]
        ordered_nodes = []

        # Pull a node from queued nodes, add it to the start of ordered nodes and add its neighbours to queued nodes
        while len(queued_nodes) > 0:
            # Remove the first node of the queued list
            node = queued_nodes.pop()
            # Insert the new node at the start
            ordered_nodes.insert(0, node)
            # Queue up the neighbours (that aren't already ordered) of this node
            queued_nodes += [n for n in self.neighbors(node) if n not in ordered_nodes and
                             isinstance(n, BronchopulmonarySegment)]

        # Process all nodes from ordered list
        while len(ordered_nodes) > 0:
            # Pull the node from the list
            node = ordered_nodes.pop(0)
            # Don't process origin - have reached the end
            if node.id == self.origin:
                break
            # Find the parent edge (should only be one) as edge where weight hasn't already been set
            # (only check bronchi)
            parent_edges = [(node1, node2, data) for node1, node2, data in self.edges(node, data=True) if
                            isinstance(data[EDGE_OBJECT], Bronchus) and data[EDGE_OBJECT].weight == 0.0]

            assert len(parent_edges) == 1
            # Get the data from parent edge to update
            parent_edge = parent_edges[0][2]
            # If the node is terminal, weight is 1.0
            if node in self.alveoli:
                parent_edge[EDGE_OBJECT].weight = 1.0
            else:
                # Get the child edges (those with weights already set) (only get bronchi)
                child_edges = [(node1, node2, data) for node1, node2, data in self.edges(node, data=True) if
                               isinstance(data[EDGE_OBJECT], Bronchus) and data[EDGE_OBJECT].weight > 0.0]

                # Get the weights
                child_orders = [data[EDGE_OBJECT].weight for _, _, data in child_edges]
                # Determine new weight based on method chosen
                if weight_method == HORSFIELD:
                    new_order = max(child_orders) + 1.0
                elif weight_method == STAHLER:
                    if len(set(child_orders)) <= 1:
                        new_order = max(child_orders) + 1.0
                    else:
                        new_order = max(child_orders)
                else:
                    raise Exception, "Invalid ordering method: {0}".format(weight_method)
                # Set the parent weight
                parent_edge[EDGE_OBJECT].weight = new_order

    def events(self):
        """ Rate of events and specific function for event - to be defined in overriding class """
        raise NotImplementedError

    def display(self, node_contents_species, title="", save_name=None, show_edge_labels=False):
        """
        Override the display method - colour nodes based on their type

        :param node_contents_species: List of species to display for nodes
        :param title:
        :param save_name: Filename to save as png
        :param show_edge_labels: Boolean to show edge labels
        :return:
        """
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
        # Bronchi nodes
        bronchi_nodes = [n for n in self.node_list.values() if isinstance(n, BronchopulmonarySegment)]
        nx.draw_networkx_nodes(self, nodelist=bronchi_nodes, pos=pos, node_size=400, node_color="red")

        # Lymph nodes
        lymph_nodes = [n for n in self.node_list.values() if isinstance(n, LymphNode)]
        nx.draw_networkx_nodes(self, nodelist=lymph_nodes, pos=pos, node_shape='p', node_size=200, node_color="white")

        # Node labels
        nx.draw_networkx_labels(self, pos, labels=node_labels, font_family='sans-serif')

        # Edges
        bronchi_edges = [(e1,e2) for (e1,e2,data) in self.edges(data=True) if isinstance(data[EDGE_OBJECT], Bronchus)]
        nx.draw_networkx_edges(self, edgelist=bronchi_edges, pos=pos, edge_color='red')
        lymph_edges = [(e1, e2) for (e1, e2, data) in self.edges(data=True)
                       if isinstance(data[EDGE_OBJECT], LymphaticVessel)]
        nx.draw_networkx_edges(self, edgelist=lymph_edges, pos=pos, edge_color='white')
        drain_edges = [(e1, e2) for (e1, e2, data) in self.edges(data=True)
                       if isinstance(data[EDGE_OBJECT], Drainage)]
        nx.draw_networkx_edges(self, edgelist=drain_edges, pos=pos, edge_color='green')

        # Edge labels
        if show_edge_labels:
            edge_labels = {}
            for n1, n2, data in self.edges(data=True):
                edge_labels[(n1, n2)] = str(data[EDGE_OBJECT])
            nx.draw_networkx_edge_labels(self, pos, edge_labels=edge_labels, font_family='sans-serif')

        plt.show()
        if save_name is not None:
            fig.savefig(save_name + ".png")  # save as png

if __name__ == '__main__':
    n = LungLymphMetapopulationNetwork(['a','b'],{},['a','b'],{})
    n.display([])

