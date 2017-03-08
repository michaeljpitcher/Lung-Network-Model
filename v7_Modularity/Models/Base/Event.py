__author__ = "Michael J. Pitcher"

import numpy as np

class Event:

    def __init__(self, probability):
        self.total = 0
        self.probability = probability

    def update_total_for_node(self, node):
        self.total += self.increment_from_node(node)

    def increment_from_node(self, node):
        raise NotImplementedError

    def perform(self, network):
        # Choose node
        r = np.random.random() * self.total
        chosen_node = None

        running_total = 0
        for node in network.node_list:
            running_total += self.increment_from_node(node)
            if running_total > r:
                chosen_node = node
                break

        self.action(chosen_node, network)

    def action(self, node, network):
        raise NotImplementedError

    def get_rate(self):
        return self.total * self.probability
