from typing import List

from distributed_environment_builder.infrastructure.network_dfg_miner import Network
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph

class NetworkAccessDfgMiner:

    def __init__(self, node_id, network, topology):
        self.network = network
        self.node_id = node_id
        self.topology: Network = topology

    def get_latest_event_with_case_id(self, case_id):
        result = []
        for node in self.topology.get_all_nodes_with_protocol(self.node_id, "sensor"):
            self.network.send(payload=1)
            latest_event = node.get_latest_event_with_case_id(case_id)
            if latest_event:
                result.append(latest_event)
        return result

    def get_directly_follows_graph(self) -> List[DirectlyFollowsGraph]:
        result = []
        for node in self.topology.get_all_nodes_with_protocol(self.node_id, "sensor"):
            self.network.send(payload=1)
            result.append(node.get_directly_follows_graph())
        return result
