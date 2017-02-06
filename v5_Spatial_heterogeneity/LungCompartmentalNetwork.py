from CompartmentalMetapopNetwork import *


class LungNetwork(CompartmentalMetapopulationNetwork):
    """
    CompartmentalMetapopulation model with a specific topology - i.e. that of the central airways of the human lung
    Also includes methods to weight the edges based on Horsfield/Stahler methods
    """

    def __init__(self, time_limit, compartments, initial_loads, weight_method='horsfield'):

        # Trachea
        edges = [(0, 1)]
        # Main bronchi
        edges += [(1, 2), (2, 3), (1, 4)]
        # Lobar bronchi
        edges += [(2, 5), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10), (10, 11), (4, 12), (12, 13), (12, 14), (4, 15),
                  (15, 16), (16, 17)]
        # Segmental bronchi
        edges += [(5, 18), (6, 19), (6, 20), (7, 21), (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27), (13, 28),
                  (13, 29), (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]

        edge_weights = {}
        for e in edges:
            edge_weights[e] = 0.0

        # Node positions TODO: done by eye
        pos = dict()
        pos[0] = (5, 10)
        pos[1] = (5, 8)
        pos[2] = (4, 7)
        pos[3] = (3.5, 5)
        pos[4] = (6, 6)
        pos[5] = (3, 8)
        pos[6] = (2.75, 8.5)
        pos[7] = (2.5, 5)
        pos[8] = (4, 4)
        pos[9] = (3.5, 3)
        pos[10] = (3, 2.5)
        pos[11] = (2.5, 2)
        pos[12] = (7, 7)
        pos[13] = (7.5, 8)
        pos[14] = (8, 7)
        pos[15] = (6.5, 5)
        pos[16] = (7.5, 4)
        pos[17] = (8, 3.5)
        pos[18] = (2.5, 7.5)
        pos[19] = (2.5, 9)
        pos[20] = (3, 9)
        pos[21] = (2, 5.5)
        pos[22] = (2, 4)
        pos[23] = (3.5, 4.25)
        pos[24] = (4, 2)
        pos[25] = (2.5, 3.25)
        pos[26] = (1.5, 1)
        pos[27] = (2.75, 1)
        pos[28] = (7.25, 8.5)
        pos[29] = (8, 8.5)
        pos[30] = (8.5, 7.5)
        pos[31] = (8.5, 6.5)
        pos[32] = (7, 5.5)
        pos[33] = (7.5, 3)
        pos[34] = (8.5, 4.25)
        pos[35] = (8.5, 3)

        # Attributes of each patch
        patch_attributes = self.compute_attributes(pos)

        # Create the network (allows use of networkx functions like neighbours for calculating edge weights)
        CompartmentalMetapopulationNetwork.__init__(self, 36, edge_weights, time_limit, compartments, initial_loads,
                                                    patch_attributes, pos)

        # Origin and terminal nodes (to compute edge weights)
        self.origin = 0
        self.terminal_nodes = [n for n in self.nodes() if self.degree(n) == 1 and n.id != self.origin]
        self.non_terminal_nodes = [n for n in self.nodes() if self.degree(n) != 1]
        # Calculate edge weights
        self.set_weights(weight_method)

    def set_weights(self, weight_method):
        """
        Set edge weights. Terminal branches order 1. Other branches depend on ordering method:
        Horsfield - parent branch has order 1 greater than maximum of child branches
        Stahler - parent branch has order 1 greater than child branches if they are equal, else has max of child orders
        :return:
        """

        # Get the nodes in an ordered list - gives a list where all child nodes appear in list before parent
        # So can add the order of an edge as all child edges (those futher from origin) will already have been computed

        # Start with origin node
        queued_nodes = [self.node_list[self.origin]]
        ordered_nodes = []

        # Pull a node from queued nodes, add it to the start of ordered nodes and add its neighbours to queued nodes
        while len(queued_nodes) > 0:
            node = queued_nodes.pop()
            ordered_nodes.insert(0, node)
            queued_nodes += [n for n in self.neighbors(node) if n not in ordered_nodes]

        # Process all nodes
        while len(ordered_nodes) > 0:
            # Pull the node from the list
            node = ordered_nodes.pop(0)
            # Don't process origin
            if node.id == self.origin:
                break
            # Find the parent edge (should only be one) as edge where weight hasn't already been set
            parent_edges = [(node1, node2, data) for node1, node2, data in self.edges(node, data=True) if
                            data['weight'] == 0.0]
            assert len(parent_edges) == 1
            # Get the data from parent edge to update
            parent_edge = parent_edges[0][2]
            # If the node is terminal, weight is 1.0
            if node in self.terminal_nodes:
                parent_edge['weight'] = 1.0
            else:
                # Get the child edges (those with weights already set)
                child_edges = [(node1, node2, data) for node1, node2, data in self.edges(node, data=True) if
                               data['weight'] > 0.0]
                # Get the weights
                child_orders = [data['weight'] for _,_,data in child_edges]
                # Determine new weight based on method chosen
                if weight_method == 'horsfield':
                    new_order = max(child_orders) + 1.0
                elif weight_method == 'stahler':
                    if len(set(child_orders)) <= 1:
                        new_order = max(child_orders) + 1.0
                    else:
                        new_order = max(child_orders)
                else:
                    raise Exception, "Invalid ordering method: {0}".format(weight_method)
                # Set the parent weight
                parent_edge['weight'] = new_order

    def compute_attributes(self, positions):
        patch_attributes = dict()
        for node_id in range(36):
            patch_attributes[node_id] = dict()
            # TODO - find out specifics
            # V - Ventilation - O2 reaching the alveolar tissue
            patch_attributes[node_id]['ventilation'] = 1.0 / positions[node_id][1]
            # Q - Perfusion - blood that reaches the alveolar tissue
            patch_attributes[node_id]['perfusion'] = 1.0 / positions[node_id][1]
            # V/Q - Ventilation Perfusion ratio
            patch_attributes[node_id]['oxygen_tension'] = patch_attributes[node_id]['ventilation'] / \
                                                          patch_attributes[node_id]['perfusion']
        return patch_attributes

    def transitions(self):
        raise NotImplementedError


