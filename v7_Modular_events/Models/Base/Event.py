__author__ = "Michael J. Pitcher"

import numpy as np

class Event:

    def __init__(self, probability):
        self.probability = probability
        self.total = 0

    def get_rate(self):
        return self.probability * self.total

    def increment_total_from_node(self, node):
        raise NotImplementedError

    def perform(self, network):
        # Choose node
        r = np.random.random() * self.total

        running_total = 0
        for node in network.node_list:
            running_total += self.increment_total_from_node(node)
            if running_total > r:
                self.update_network(node, network)
                return

    def update_network(self, chosen_node, network):
        raise NotImplementedError
