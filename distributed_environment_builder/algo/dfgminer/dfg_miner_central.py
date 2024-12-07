from distributed_environment_builder.algo.dfgminer.hardware.cpu_dfg_miner import CpuDfgMiner
from distributed_environment_builder.algo.dfgminer.hardware.storage_dfg_miner import StorageDfgMiner
from distributed_environment_builder.benchmark.abstract_algorithm import AbstractAlgorithm
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology
from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event


class DfgMinerCentral(AbstractAlgorithm):

    def __init__(self):
        self.cpu: CpuDfgMiner = None
        self.storage = None
        self.network_intermediary = None
        self.network_source_list = []

    def assign_to_node(
            self,
            node_id,
            computing_topology: ComputingTopology):

        computing_node = computing_topology.get_computing_node(node_id)
        self.cpu: CpuDfgMiner = CpuDfgMiner(computing_node.cpu)
        self.storage = StorageDfgMiner(computing_node.memory)

    def receive_event(self, event: Event):
        last_event = self.storage.get_latest_event_with_case_id(event.caseid)
        self.storage.store_event(event)
        if not last_event:
            last_activity = "<start>"
        else:
            last_activity = last_event.activity
        self.storage.store_directly_follows_relation(DirectlyFollowsRelation(last_activity, event.activity))

    def get_directly_follows_graph_request(self):
        return self.cpu.build_dfg(self.storage.get_all_directly_follows_relations())

