from typing import List

from distributed_environment_builder.algo.dfgminer.hardware.cpu_dfg_miner import CpuDfgMiner
from distributed_environment_builder.benchmark.abstract_algorithm import Algorithm
from distributed_environment_builder.algo.dfgminer.hardware.network_access_dfg_miner import NetworkAccessDfgMiner
from distributed_environment_builder.algo.dfgminer.hardware.network_access_dfg_miner_intermediary import NetworkAccessDfgMinerIntermediary
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph

class DfgMinerIntermediary(Algorithm):

    def __init__(self):
        super().__init__(protocol_ids=["fog"])
        self.cpu = None
        self.network_intermediary = None
        self.network_source_list = []

    def assign_to_node(
            self,
            node_id,
            computing_topology: ComputingTopology):
        
        computing_node = computing_topology.get_computing_node(node_id)
        self.cpu: CpuDfgMiner = CpuDfgMiner(computing_node.cpu)

        self.network_source_list: List[NetworkAccessDfgMiner] = (
            [NetworkAccessDfgMiner(node_id,computing_node.network, network)
            for network in computing_topology.get_labeled_network_list_for_computing_node("sensor", node_id)
        ])
        self.network_intermediary: NetworkAccessDfgMinerIntermediary = NetworkAccessDfgMinerIntermediary(
            node_id,
            computing_node.network,
            computing_topology.get_labeled_network_for_computing_node("intermediary", node_id)
        )

    def get_directly_follows_graph_request(self):
        resulting_directly_follows_graphs = self.network_intermediary.get_directly_follows_graph()
        resulting_directly_follows_graphs.append(self.get_directly_follows_graph())
        return self.merge_sub_dfgs(resulting_directly_follows_graphs)

    def get_directly_follows_graph(self) -> DirectlyFollowsGraph:
        return self.merge_sub_dfgs(self.network_source_list[0].get_directly_follows_graph())

    def merge_sub_dfgs(self, directly_follows_graphs: List[DirectlyFollowsGraph]):
        if not directly_follows_graphs:
            return None
        resulting_directly_follows_graph = directly_follows_graphs[0]
        for dfg in directly_follows_graphs:
            resulting_directly_follows_graph = self.cpu.merge_dfgs(resulting_directly_follows_graph, dfg)
        return resulting_directly_follows_graph
