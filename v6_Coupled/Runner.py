from Models.TB.TB_FSIcRIn import *
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
parameters[MACROPHAGES_PER_BPS] = 50
parameters[MACROPHAGES_PER_LYMPH] = 10

parameters[P_REPLICATE_FAST] = 0.1
parameters[P_REPLICATE_SLOW] = 0.01
parameters[P_REPLICATE_INTRACELLULAR] = 0.1
parameters[P_MIGRATE_FAST] = 0.0
parameters[P_MIGRATE_SLOW] = 0.0
parameters[P_CHANGE_FAST_TO_SLOW] = 0.0
parameters[P_CHANGE_SLOW_TO_FAST] = 0.0
parameters[P_BPS_RECRUIT_MACROPHAGE] = 0.01*50
parameters[P_LYMPH_RECRUIT_MACROPHAGE] = 0.01*10
parameters[P_DEATH_REGULAR_MACROPHAGE] = 0.01
parameters[P_DEATH_INFECTED_MACROPHAGE] = 0.1
parameters[P_REGULAR_MACROPHAGE_INGEST_FAST] = 0.01
parameters[P_REGULAR_MACROPHAGE_INGEST_SLOW] = 0.01
parameters[P_INFECTED_MACROPHAGE_INGEST_FAST] = 0.01
parameters[P_INFECTED_MACROPHAGE_INGEST_SLOW] = 0.01
parameters[P_MIGRATE_REGULAR_MACROPHAGE] = 0.00
parameters[P_MIGRATE_INFECTED_MACROPHAGE] = 0.9

a = TB_FSIcRIn(positions=node_positions, parameters=parameters)

a.run(50)
a.display([MACROPHAGE_INFECTED])
