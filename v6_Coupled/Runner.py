from Models.Lung.LungLymph import LungLymph
import ConfigParser

BPS_POSITIONS = 'BronchopulmonarySegmentPositions'
LN_POSITIONS = 'LymphNodePositions'

position_config_filename = 'node_positions.properties'

# Check the config file for node positions is set up
node_pos_config = ConfigParser.RawConfigParser()
if not node_pos_config.read(position_config_filename):
    raise IOError("Node position file ({0}) not found".format(position_config_filename))

node_positions = dict()
for i in node_pos_config.options(BPS_POSITIONS):
    node_positions[int(i)] = tuple([float(a) for a in node_pos_config.get(BPS_POSITIONS, i).split(",")])
for i in node_pos_config.options(LN_POSITIONS):
    node_positions[int(i)] = tuple([float(a) for a in node_pos_config.get(LN_POSITIONS, i).split(",")])

a = LungLymph(species=[], loads={}, positions=node_positions)

a.display([])