from distributed_environment_builder.infrastructure.network_dfg_miner import Network
from distributed_environment_builder.infrastructure.hii.network_hii import NetworkInstruction

class EdgeMineNetwork:

    def __init__(self, own_node_id, topology, network):
        self.topology: Network = topology
        self.own_node_id: str = own_node_id
        self.network: NetworkInstruction = network

    def get_latest_activity_with_case_id(self, case_id):
        predecessors = []
        for node in self.topology.get_all_nodes_with_protocol(self.own_node_id, protocol_label="sensor"):
            self.network.send(1)
            node.get_latest_event_with_case_id(case_id)
        return predecessors

    def get_latest_activity_with_case_id_mfp(self, case_id, node_id):
        self.network.send(1)
        return self.topology.get_node(node_id).get_latest_activity_with_case_id(case_id)
            
    def inform_predecessor(self, case_id, node_id, activity):
        self.network.send(1)
        self.topology.get_node(node_id).inform_predecessor(case_id, node_id, activity)

    def get_directly_follows_graph(self):
        result = []
        for node in self.topology.get_all_nodes_with_protocol(self.own_node_id, protocol_label="sensor"):
            self.network.send(1)
            result.append(node.get_directly_follows_graph())
        return result

    def get_all_node_ids(self):
        return self.topology.get_all_node_ids()
