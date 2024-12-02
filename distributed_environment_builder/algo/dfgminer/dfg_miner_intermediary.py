from typing import List

from distributed_environment_builder.platform.abstract_algorithm import AbstractAlgorithm
from distributed_environment_builder.algo.dfgminer.hardware.network_access_dfg_miner import NetworkAccessDfgMiner
from distributed_environment_builder.algo.dfgminer.hardware.network_access_dfg_miner_intermediary import NetworkAccessDfgMinerIntermediary
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology
from process_mining_core.datastructure.converter.directly_follows_graph_merger import DirectlyFollowsGraphMerger
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph

class DfgMinerIntermediary(AbstractAlgorithm):

    def __init__(self):
        self.network_intermediary = None
        self.network_source = None

    def assign_to_node(
            self,
            node_id,
            computing_topology: ComputingTopology):
        
        computing_node = computing_topology.get_computing_node(node_id)
        self.network_source: NetworkAccessDfgMiner = NetworkAccessDfgMiner(
            node_id,
            computing_node.network,
            computing_topology.get_labeled_network_for_computing_node("sensor", node_id)
        )
        self.network_intermediary: NetworkAccessDfgMinerIntermediary = NetworkAccessDfgMinerIntermediary(
            node_id,
            computing_node.network,
            computing_topology.get_labeled_network_for_computing_node("intermediary", node_id)
        )

    def get_directly_follows_graph_request(self):
        resulting_directly_follows_graphs = []
        resulting_directly_follows_graphs.append(self.get_directly_follows_graph())
        resulting_directly_follows_graphs.extend(self.network_intermediary.get_directly_follows_graph())
        return self.merge_sub_dfgs(resulting_directly_follows_graphs)

    def get_directly_follows_graph(self) -> DirectlyFollowsGraph:
        return self.merge_sub_dfgs(self.network_source.get_directly_follows_graph())

    def merge_sub_dfgs(self, directly_follows_graphs: List[DirectlyFollowsGraph]):
        if not directly_follows_graphs:
            return None
        resulting_directly_follows_graph = directly_follows_graphs[0]
        for dfg in directly_follows_graphs:
            resulting_directly_follows_graph = DirectlyFollowsGraphMerger().merge_directly_follows_graph(dfg, resulting_directly_follows_graph)
        return resulting_directly_follows_graph