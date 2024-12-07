from typing import Dict, Any, List

from distributed_environment_builder.algo.dfgminer.hardware.network_access_dfg_miner_cloud_sensor import \
    NetworkAccessDfgMinerCloudSensor
from distributed_environment_builder.benchmark.abstract_algorithm import AbstractAlgorithm
from distributed_environment_builder.algo.dfgminer.hardware.cpu_dfg_miner import CpuDfgMiner
from distributed_environment_builder.algo.dfgminer.hardware.network_access_dfg_miner import NetworkAccessDfgMiner
from distributed_environment_builder.algo.dfgminer.hardware.storage_dfg_miner import StorageDfgMiner
from distributed_environment_builder.algo.dfgminer.dfg_miner_abstract import AbstractDfgMiner
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology
from process_mining_core.datastructure.converter.directly_follows_graph_merger import DirectlyFollowsGraphMerger
from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph


class DfgMinerCloudSensor(AbstractAlgorithm):
    def __init__(
            self
    ):
        super().__init__()
        self.network: NetworkAccessDfgMinerCloudSensor = None
        self.storage = None
        self.cpu = None

    def assign_to_node(
            self,
            node_id,
            computing_topology: ComputingTopology):
        computing_node = computing_topology.get_computing_node(node_id)
        network_access = computing_topology.get_labeled_network_for_computing_node("cloud", computing_node.get_name())
        self.network: NetworkAccessDfgMinerCloudSensor = NetworkAccessDfgMinerCloudSensor(node_id, computing_node.network, network_access)

    def receive_event(self, incoming_event: Event):
        self.network.send_event(incoming_event)