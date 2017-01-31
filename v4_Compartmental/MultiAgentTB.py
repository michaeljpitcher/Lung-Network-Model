from LungCompartmentalNetwork import *

fast_bac = 'F'
slow_bac = 'S'
int_bac = 'I_b'
rest_mac = 'R'
act_mac = 'A'
inf_mac = 'I_m'
chrinf_mac = 'C'
rate_repl_fast = 'replication_fast'
rate_repl_slow = 'replication_slow'
rate_ingest_rest_fast = 'resting_ingests_fast'
rate_ingest_rest_slow = 'resting_ingests_slow'
rate_ingest_act_fast = 'active_ingests_fast'
rate_ingest_act_slow = 'active_ingests_slow'
rate_ingest_inf_fast = 'infected_ingests_fast'
rate_ingest_inf_slow = 'infected_ingests_slow'
rate_ingest_chrinf_fast = 'chronically_infected_ingests_fast'
rate_ingest_chrinf_slow = 'chronically_infected_ingests_slow'
rate_recruit = 'recruit_macrophage'
rate_activate = 'resting_activation'
rate_deact = 'active_deactivation'
rate_death_rest = 'resting_death'
rate_death_act = 'active_death'
rate_death_inf = 'infected_death'
rate_death_chrinf = 'chr_infected_death'
rate_change_fast_to_slow = 'change_fast_to_slow'
rate_change_slow_to_fast = 'change_slow_to_fast'
rate_translocate_fast = 'fast_translocate'
rate_translocate_slow = 'slow_translocate'


class TBMultiAgentMetapopulationNetwork(LungNetwork):

    def __init__(self, rates, time_limit, initial_loads, weight_method='horsfield'):

        compartments_bac = [fast_bac, slow_bac, int_bac]
        compartments_mac = [rest_mac, act_mac, inf_mac, chrinf_mac]

        # Create the network (allows use of networkx functions like neighbours for calculating edge weights)
        LungNetwork.__init__(self, time_limit, compartments_bac + compartments_mac, initial_loads, weight_method)

        # Assert all rates present
        expected_rates = [rate_repl_fast, rate_repl_slow,
                          rate_ingest_rest_fast, rate_ingest_rest_slow,
                          rate_ingest_act_fast, rate_ingest_act_slow,
                          rate_ingest_inf_fast, rate_ingest_inf_slow,
                          rate_ingest_chrinf_fast, rate_ingest_chrinf_slow,
                          rate_recruit,
                          rate_activate, rate_deact,
                          rate_death_rest, rate_death_act, rate_death_inf, rate_death_chrinf,
                          rate_change_fast_to_slow, rate_change_slow_to_fast,
                          rate_translocate_fast, rate_translocate_slow]

        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

        self.total_f = 0
        self.total_s = 0
        self.total_f_r = 0
        self.total_s_r = 0
        self.total_r = 0
        self.total_f_a = 0
        self.total_s_a = 0
        self.total_a = 0
        self.total_i_m = 0
        self.total_f_im = 0
        self.total_s_im = 0
        self.total_c = 0
        self.total_f_degree = 0
        self.total_s_degree = 0

    def transitions(self):

        transitions = []

        self.total_f = sum([node.counts[fast_bac] for node in self.nodes()])
        self.total_s = sum([node.counts[slow_bac] for node in self.nodes()])
        self.total_f_r = sum([node.counts[fast_bac] * node.counts[rest_mac] for node in self.nodes()])
        self.total_s_r = sum([node.counts[slow_bac] * node.counts[rest_mac] for node in self.nodes()])
        self.total_r = sum([node.counts[rest_mac] for node in self.nodes()])
        self.total_f_a = sum([node.counts[fast_bac] * node.counts[act_mac] for node in self.nodes()])
        self.total_s_a = sum([node.counts[slow_bac] * node.counts[act_mac] for node in self.nodes()])
        self.total_a = sum([node.counts[act_mac] for node in self.nodes()])
        self.total_i_m = sum([node.counts[inf_mac] for node in self.nodes()])
        self.total_f_im = sum([node.counts[fast_bac] * node.counts[inf_mac] for node in self.nodes()])
        self.total_s_im = sum([node.counts[slow_bac] * node.counts[inf_mac] for node in self.nodes()])
        self.total_f_c = sum([node.counts[fast_bac] * node.counts[chrinf_mac] for node in self.nodes()])
        self.total_s_c = sum([node.counts[slow_bac] * node.counts[chrinf_mac] for node in self.nodes()])
        self.total_c = sum([node.counts[chrinf_mac] for node in self.nodes()])
        # TODO - check usage of degree
        self.total_f_degree = sum([node.counts[fast_bac] * self.degree(node) for node in self.nodes()])
        self.total_s_degree = sum([node.counts[slow_bac] * self.degree(node) for node in self.nodes()])

        # Replication (FAST)
        transitions.append((self.total_f * self.rates[rate_repl_fast], self.replicate(fast_bac)))
        # Replication (SLOW)
        transitions.append((self.total_f * self.rates[rate_repl_slow], self.replicate(fast_bac)))

        # Resting ingests fast
        transitions.append((self.total_f_r * self.rates[rate_ingest_rest_fast], self.ingests(rest_mac, fast_bac)))
        # Resting ingests slow
        transitions.append((self.total_s_r * self.rates[rate_ingest_rest_fast], self.ingests(rest_mac, slow_bac)))
        # Active ingests fast
        transitions.append((self.total_f_a * self.rates[rate_ingest_act_fast], self.ingests(act_mac, fast_bac)))
        # Active ingests slow
        transitions.append((self.total_s_a * self.rates[rate_ingest_act_slow], self.ingests(act_mac, slow_bac)))
        # Inf ingests fast
        transitions.append((self.total_f_im * self.rates[rate_ingest_inf_fast], self.ingests(inf_mac, fast_bac)))
        # Inf ingests slow
        transitions.append((self.total_s_im * self.rates[rate_ingest_inf_slow], self.ingests(inf_mac, slow_bac)))
        # Chr Inf ingests fast
        transitions.append((self.total_f_c * self.rates[rate_ingest_inf_fast], self.ingests(inf_mac, fast_bac)))
        # Chr Inf ingests slow
        transitions.append((self.total_s_ic * self.rates[rate_ingest_inf_slow], self.ingests(inf_mac, slow_bac)))

        # Recruit mac
        # TODO - this should probably be based on the level of infection
        transitions.append((len(self.nodes()) * self.rates[rate_recruit], self.recruit_mac()))

        # Activate mac
        # TODO - this should probably be based on the level of infection
        transitions.append((self.total_r * self.rates[rate_activate], self.activate()))

        # Dectivate mac
        # TODO - this should probably be based on the level of infection
        transitions.append((self.total_a * self.rates[rate_deact], self.deactivate()))

        # Death of mac
        # Resting
        transitions.append((self.total_r * self.rates[rate_death_rest], self.death_mac(rest_mac)))
        # Active
        transitions.append((self.total_a * self.rates[rate_death_act], self.death_mac(act_mac)))
        # Inf
        transitions.append((self.total_i_m * self.rates[rate_death_inf], self.death_mac(inf_mac)))
        # Chr Inf
        transitions.append((self.total_c * self.rates[rate_death_chrinf], self.death_mac(chrinf_mac)))

        # TODO - should metabolism change be constant rate?
        # Metabolism change
        transitions.append((self.total_f * self.rates[rate_change_fast_to_slow], self.change(slow_bac)))
        transitions.append((self.total_s * self.rates[rate_change_slow_to_fast], self.change(fast_bac)))

        # Translocate
        transitions.append((self.total_f_degree * self.rates[rate_translocate_fast], self.translocate(fast_bac)))
        transitions.append((self.total_s_degree * self.rates[rate_translocate_slow], self.translocate(slow_bac)))

    def replicate(self, metabolism):
        if metabolism == fast_bac:
            r = np.random.random() * self.total_f
            rate = self.rates[rate_repl_fast]
        elif metabolism == slow_bac:
            r = np.random.random() * self.total_s
            rate = self.rates[rate_repl_slow]
        else:
            raise Exception, "Invalid replication: {0} metabolism not valid".format(type)

        running_total = 0
        for node in self.nodes():
            running_total += node.counts[metabolism]
            if running_total >= r:
                if rate > 0:
                    self.update_node(node, metabolism, 1)
                elif rate < 0:
                    self.update_node(node, metabolism, -1)
                return

    def ingests(self, mac_state, metabolism):
        if metabolism == fast_bac:
            if mac_state == rest_mac:
                total = self.total_f_r
            elif mac_state == act_mac:
                total = self.total_f_a
            elif mac_state == inf_mac:
                total = self.total_f_im
            elif mac_state == chrinf_mac:
                total = self.total_f_c
            else:
                raise Exception, "Invalid ingest: {0} not valid".format(mac_state)
        elif metabolism == slow_bac:
            if mac_state == rest_mac:
                total = self.total_s_r
            elif mac_state == act_mac:
                total = self.total_s_a
            elif mac_state == inf_mac:
                total = self.total_s_im
            elif mac_state == chrinf_mac:
                total = self.total_s_c
            else:
                raise Exception, "Invalid ingest: {0} not valid".format(mac_state)
        else:
            raise Exception, "Invalid ingest: {0} not valid".format(metabolism)

        r = np.random.random() * total

        running_total = 0
        for node in self.nodes():
            running_total += node.counts[metabolism] * node.counts[mac_state]
            if running_total >= r:
                self.update_node(node, metabolism, -1)
                if mac_state != act_mac:
                    self.update_node(node, int_bac, 1)
                    if mac_state == rest_mac:
                        self.update_node(node, rest_mac, -1)
                        self.update_node(node, inf_mac, 1)
                # TODO - inf to chrinf? chrinf bursts?
                return

    def recruit_mac(self):
        # TODO - as above, based on level of infection?
        node = np.random.choice(self.nodes(),1)
        self.update_node(node, rest_mac, 1)

    def activate(self):
        r = np.random.randint(0, self.total_r)
        running_total = 0
        for node in self.nodes():
            running_total += node.counts[rest_mac]
            if running_total >= r:
                self.update_node(node, act_mac, 1)
                self.update_node(node, rest_mac, -1)
                return

    def deactivate(self):
        r = np.random.randint(0, self.total_a)
        running_total = 0
        for node in self.nodes():
            running_total += node.counts[act_mac]
            if running_total >= r:
                self.update_node(node, rest_mac, 1)
                self.update_node(node, act_mac, -1)
                return

    def death_mac(self, state):
        if state == rest_mac:
            r = np.random.randint(0, self.total_r)
        elif state == act_mac:
            r = np.random.randint(0, self.total_a)
        elif state == inf_mac:
            r = np.random.randint(0, self.total_i_m)
        elif state == chrinf_mac:
            r = np.random.randint(0, self.total_c)
        else:
            raise Exception, "Invalid death: {0} not valid".format(state)

        running_total = 0
        for node in self.nodes():
            running_total += node.counts[state]
            if running_total >= r:
                self.update_node(node, state, -1)
                # TODO maybe add caseum
                return

    def translocate(self, metabolism):
        # TODO - check usage of degree / weights
        if metabolism == fast_bac:
            r = np.random.randint(0, self.total_f_degree)
        elif metabolism == slow_bac:
            r = np.random.randint(0, self.total_s_degree)
        else:
            raise Exception, "Invalid translocate: {0} not valid".format(metabolism)

        running_total = 0
        for node in self.nodes():
            running_total += node.counts[metabolism]
            if running_total >= r:
                total_weights = sum(d['weight'] for _, _, d in self.edges(node, data=True))
                r2 = np.random.random() * total_weights
                running_total_weights = 0
                for _, neighbour, edge in self.edges(node, data=True):
                    running_total_weights += edge['weight']
                    if running_total_weights > r2:
                        self.update_node(node, metabolism, -1)
                        self.update_node(neighbour, metabolism, 1)
                        return

    def change(self, new_metabolism):
        if new_metabolism == fast_bac:
            r = np.random.random() * self.total_s
            old_metabolism = slow_bac
        elif new_metabolism == slow_bac:
            r = np.random.random() * self.total_f
            old_metabolism = fast_bac
        else:
            raise Exception, "Invalid metabolism change: {0} metabolism not valid".format(new_metabolism)

        running_total = 0
        for node in self.nodes():
            running_total += node.counts[old_metabolism]
            if running_total >= r:
                self.update_node(node, new_metabolism, 1)
                self.update_node(node, old_metabolism, -1)
                return


if __name__ == '__main__':
    rates = dict()
    rates[fast_bac] = 0.0
    rates[slow_bac] = 0.0
    rates[int_bac] = 0.0
    rates[rest_mac] = 0.0
    rates[act_mac] = 0.0
    rates[inf_mac] = 0.0
    rates[chrinf_mac] = 0.0
    rates[rate_repl_fast] = 0.0
    rates[rate_repl_slow] = 0.0
    rates[rate_ingest_rest_fast] = 0.0
    rates[rate_ingest_rest_slow] = 0.0
    rates[rate_ingest_act_fast] = 0.0
    rates[rate_ingest_act_slow] = 0.0
    rates[rate_ingest_inf_fast] = 0.0
    rates[rate_ingest_inf_slow] = 0.0
    rates[rate_ingest_chrinf_fast] = 0.0
    rates[rate_ingest_chrinf_slow] = 0.0
    rates[rate_recruit] = 0.0
    rates[rate_activate] = 0.0
    rates[rate_deact] = 0.0
    rates[rate_death_rest] = 0.0
    rates[rate_death_act] = 0.0
    rates[rate_death_inf] = 0.0
    rates[rate_death_chrinf] = 0.0
    rates[rate_translocate_fast] = 0.0
    rates[rate_translocate_slow] = 0.0

    loads = dict()

    netw = TBMultiAgentMetapopulationNetwork(rates, 10, loads)

    netw.display(show_node_contents=False, show_edge_labels=False)





