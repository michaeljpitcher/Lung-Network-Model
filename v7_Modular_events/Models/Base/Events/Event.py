__author__ = "Michael J. Pitcher"

import numpy as np


class Event:
    """ Abstract class to perform an event over a metapopulation network.

    Events have user-defined probabilities, and a specific total which is determined in some way by the current state
    of the network. The total is updated by investigating each node in turn and calling the increment_from_node function
    which is used to increase the total in some manner (e.g. by counting member of a class at the node). The full total
    is then multiplied by the probability to create a rate, which is used to determine if the event occurs. If it does,
    the perform method is called. This picks a node for the event to take place, using the same functionality as is used
    to create the total (i.e. increment_from_node). When a node is picked, update_network is called to change the
    network in some way at the chosen node.

    """

    def __init__(self, probability):
        self.probability = probability
        self.total = 0

    def get_rate(self):
        """
        Rate is the set probability * the total count
        :return:
        """
        return self.probability * self.total

    def increment_from_node(self, node, network):
        raise NotImplementedError

    def perform(self, network):
        """ Choose a node and update it and any other relevant nodes on the network
        :param network: The network to be updated
        :return:
        """
        # Choose node by using the same increment function as used for the total
        r = np.random.random() * self.total
        running_total = 0
        for node in network.node_list:
            running_total += self.increment_from_node(node, network)
            # Node has been chosen
            if running_total > r:
                self.update_network(node, network)
                return

    def update_network(self, chosen_node, network):
        raise NotImplementedError
