from Models.TB.TB_Full import *
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
parameters[P_REPLICATION_BACTERIA_FAST] = 0.0
parameters[P_REPLICATION_BACTERIA_SLOW] = 0.0
parameters[P_REPLICATION_BACTERIA_INTRACELLULAR] = 0.0
parameters[P_CHANGE_BACTERIA_FAST_TO_SLOW] = 0.0
parameters[P_CHANGE_BACTERIA_SLOW_TO_FAST] = 0.0
parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_FAST] = 0.0
parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_SLOW] = 0.0
parameters[P_TRANSLOCATE_LYMPH_BACTERIA_FAST] = 0.0
parameters[P_TRANSLOCATE_LYMPH_BACTERIA_SLOW] = 0.0
parameters[P_RECRUITMENT_BPS_MACROPHAGE] = 0.0
parameters[P_RECRUITMENT_LYMPH_MACROPHAGE] = 0.0
parameters[P_DEATH_MACROPHAGE_REGULAR] = 0.0
parameters[P_DEATH_MACROPHAGE_INFECTED] = 0.0
parameters[P_INGEST_AND_RETAIN_REGULAR_FAST] = 0.0
parameters[P_INGEST_AND_RETAIN_REGULAR_SLOW] = 0.0
parameters[P_INGEST_AND_RETAIN_INFECTED_FAST] = 0.0
parameters[P_INGEST_AND_RETAIN_INFECTED_SLOW] = 0.0
parameters[P_INGEST_AND_DESTROY_REGULAR_FAST] = 0.0
parameters[P_INGEST_AND_DESTROY_REGULAR_SLOW] = 0.0
parameters[P_INGEST_AND_DESTROY_INFECTED_FAST] = 0.0
parameters[P_INGEST_AND_DESTROY_INFECTED_SLOW] = 0.0

loads = dict()
for i in range(36):
    loads[i] = dict()
    loads[i][MACROPHAGE_REGULAR] = 100

a = TBMetapopulationModel(positions=node_positions, loads=loads, parameters=parameters)

a.run(50)
a.display([MACROPHAGE_REGULAR])
