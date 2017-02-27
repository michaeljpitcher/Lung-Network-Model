from Models.TB.TB_FS import *
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

parameters = dict()
parameters[FAST_BACTERIA_TO_LOAD] = 10
parameters[SLOW_BACTERIA_TO_LOAD] = 0

parameters[P_REPLICATE_FAST] = 0.0
parameters[P_REPLICATE_SLOW] = 0.0
parameters[P_MIGRATE_FAST] = 0.0
parameters[P_MIGRATE_SLOW] = 0.0
parameters[P_CHANGE_FAST_TO_SLOW] = 0.1
parameters[P_CHANGE_SLOW_TO_FAST] = 0.0

a = TB_FS(positions=node_positions, parameters=parameters)

a.run(10)
a.display([BACTERIA_FAST, BACTERIA_SLOW])
