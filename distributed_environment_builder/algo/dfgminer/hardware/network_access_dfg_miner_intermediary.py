from typing import List

from distributed_environment_builder.algo.dfgminer.hardware.network_dfg_miner import Network
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph


class NetworkAccessDfgMinerIntermediary:

    def __init__(self, node_id, network, topology):
        self.network = network
        self.node_id = node_id
        self.topology: Network = topology

    def get_directly_follows_graph(self) -> List[DirectlyFollowsGraph]:
        result = []
        for node in self.topology.get_all_nodes_intermediary(self.node_id):
            self.network.send(payload=1)
            latest_event = node.get_directly_follows_graph()
            if latest_event:
                result.append(latest_event)
        return result