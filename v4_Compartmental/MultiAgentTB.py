from LungCompartmentalNetwork import *


class TBMultiAgentMetapopulationNetwork(LungNetwork):

    def __init__(self, rates, time_limit, initial_loads, weight_method='horsfield'):

        compartments_bac = ['F', 'S', 'I_b']
        compartments_mac = ['R', 'A', 'I_m', 'CI']

        # Create the network (allows use of networkx functions like neighbours for calculating edge weights)
        LungNetwork.__init__(self, time_limit, compartments_bac + compartments_mac, initial_loads, weight_method)

        # Assert all rates present
        expected_rates = ['replication_fast', 'replication_slow',
                          'resting_ingests_fast', 'resting_ingests_slow'
                          'active_ingests_fast', 'active_ingests_slow'
                          'infected_ingests_fast', 'infected_ingests_slow'
                          'chr_infected_ingests_fast', 'chr_infected_ingests_slow'
                          'recruit_macrophage',
                          'resting_activation', 'active_deactivation',
                          'resting_death', 'active_death', 'infected_death', 'chr_infected_death', 'chr_infected_burst'
                          'fast_transmit', 'slow_transmit']

        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

        self.total_transmit_f = 0.0
        self.total_transmit_s = 0.0
        self.total_f = 0.0
        self.total_s = 0.0