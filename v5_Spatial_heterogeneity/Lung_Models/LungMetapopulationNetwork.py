from v5_Spatial_heterogeneity.Base.MetapopulationNetwork import *
from v5_Spatial_heterogeneity.Lung_Models.BronchopulmonarySegment import BronchopulmonarySegment
from v5_Spatial_heterogeneity.Lung_Models.Bronchus import Bronchus

HORSFIELD = 'horsfield'
STAHLER = 'stahler'
WEIGHT = 'weight'


class LungMetapopulationNetwork(MetapopulationNetwork):
    """
    Metapopulation model with a specific topology - i.e. that of the central airways of the human lung
    Also includes methods to weight the edges based on Horsfield/Stahler methods
    """

    def __init__(self, species_keys, initial_loads, weight_method=HORSFIELD):
        """

        :param species_keys: Indicators for species of patch subpopulations
        :param initial_loads: Dictionary defining how many of each species reside in each compartment initially.
               keys=node id, values= dictionary, keys=species, values=count of species
        :param weight_method: Method to weight the edges (Stahler or Horsfield)
        """

        # Node positions TODO: currently done by eye
        positions = dict()
        positions[0] = (5, 10)
        positions[1] = (5, 8)
        positions[2] = (4, 7)
        positions[3] = (3.5, 5)
        positions[4] = (6, 6)
        positions[5] = (3, 8)
        positions[6] = (2.75, 8.5)
        positions[7] = (2.5, 5)
        positions[8] = (4, 4)
        positions[9] = (3.5, 3)
        positions[10] = (3, 2.5)
        positions[11] = (2.5, 2)
        positions[12] = (7, 7)
        positions[13] = (7.5, 8)
        positions[14] = (8, 7)
        positions[15] = (6.5, 5)
        positions[16] = (7.5, 4)
        positions[17] = (8, 3.5)
        positions[18] = (2.5, 7.5)
        positions[19] = (2.5, 9)
        positions[20] = (3, 9)
        positions[21] = (2, 5.5)
        positions[22] = (2, 4)
        positions[23] = (3.5, 4.25)
        positions[24] = (4, 2)
        positions[25] = (2.5, 3.25)
        positions[26] = (1.5, 1)
        positions[27] = (2.75, 1)
        positions[28] = (7.25, 8.5)
        positions[29] = (8, 8.5)
        positions[30] = (8.5, 7.5)
        positions[31] = (8.5, 6.5)
        positions[32] = (7, 5.5)
        positions[33] = (7.5, 3)
        positions[34] = (8.5, 4.25)
        positions[35] = (8.5, 3)

        ventilations = dict()
        perfusions = dict()
        oxygen_tensions = dict()

        # Process each node
        for node_id in range(36):
            # TODO - find out specifics
            # V - Ventilation - O2 reaching the alveolar tissue
            ventilations[node_id] = 1.0 / positions[node_id][1]
            # Q - Perfusion - blood that reaches the alveolar tissue
            perfusions[node_id] = 1.0 / positions[node_id][1]
            # V/Q - Ventilation Perfusion ratio
            oxygen_tensions[node_id] = ventilations[node_id] / perfusions[node_id]

        nodes = []
        for id in range(36):
            if id in initial_loads:
                loads_for_node = initial_loads[id]
            else:
                # Empty dict
                loads_for_node = dict()
            # Create a bronchopulmonary segment instance
            node = BronchopulmonarySegment(id, species_keys, loads_for_node, positions[id], ventilations[id],
                                           perfusions[id], oxygen_tensions[id])
            # Add to list
            nodes.append(node)

        # List of edges - names give rough approximation of which parts of anatomy are represented
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
        # Set edge weights to zero to begin
        edge_weights = {}
        for e in edges:
            edge_weights[e] = Bronchus()

        # Create the network (allows use of NetworkX functions like neighbours for calculating edge weights)
        MetapopulationNetwork.__init__(self, nodes, edge_weights, species_keys)

        # Origin and terminal nodes (to compute edge weights)
        self.origin = 0
        self.terminal_nodes = [n for n in self.node_list.values() if n.degree == 1 and n.id != self.origin]
        self.non_terminal_nodes = [n for n in self.node_list.values() if n.degree != 1]
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
            queued_nodes += [n for n in self.neighbors(node) if n not in ordered_nodes]

        # Process all nodes from ordered list
        while len(ordered_nodes) > 0:
            # Pull the node from the list
            node = ordered_nodes.pop(0)
            # Don't process origin - have reached the end
            if node.id == self.origin:
                break
            # Find the parent edge (should only be one) as edge where weight hasn't already been set
            parent_edges = [(node1, node2, data) for node1, node2, data in self.edges(node, data=True) if
                            data[EDGE_OBJECT].weight == 0.0]
            assert len(parent_edges) == 1
            # Get the data from parent edge to update
            parent_edge = parent_edges[0][2]
            # If the node is terminal, weight is 1.0
            if node in self.terminal_nodes:
                parent_edge[EDGE_OBJECT].weight = 1.0
            else:
                # Get the child edges (those with weights already set)
                child_edges = [(node1, node2, data) for node1, node2, data in self.edges(node, data=True) if
                               data[EDGE_OBJECT].weight > 0.0]
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


