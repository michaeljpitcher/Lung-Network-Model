from ..Base.MetapopulationNetwork import MetapopulationNetwork

class LungLymph(MetapopulationNetwork):

    def __init__(self, species):

        # node_pos_config = ConfigParser.RawConfigParser()
        # if not node_pos_config.read('node_positions.properties'):
        #     raise IOError("Config file (node_positions.properties) not found")

        nodes = []
        # nodes += self.bronchial_edges(node_pos_config)

        edges = []

        MetapopulationNetwork.__init__(self, nodes, edges, species)

    def bronchial_edges(self, node_pos_config):
        # BPS
        for i in node_pos_config.options("BronchopulmonarySegmentPositions"):
            print i

if __name__ == '__main__':
    a = LungLymph(['a'])