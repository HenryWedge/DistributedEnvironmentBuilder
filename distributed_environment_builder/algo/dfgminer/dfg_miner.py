from typing import Dict, Any, List

from distributed_environment_builder.benchmark.abstract_algorithm import Algorithm
from distributed_environment_builder.algo.dfgminer.hardware.cpu_dfg_miner import CpuDfgMiner
from distributed_environment_builder.algo.dfgminer.hardware.network_access_dfg_miner import NetworkAccessDfgMiner
from distributed_environment_builder.algo.dfgminer.hardware.storage_dfg_miner import StorageDfgMiner
from distributed_environment_builder.algo.dfgminer.dfg_miner_abstract import AbstractDfgMiner
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology
from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph


class DfgMiner(AbstractDfgMiner, Algorithm):
    def __init__(
            self
    ):
        super().__init__(["sensor"])
        self.network = None
        self.storage = None
        self.cpu = None

    def assign_to_node(
            self,
            node_id,
            computing_topology: ComputingTopology):
        computing_node = computing_topology.get_computing_node(node_id)
        self.cpu: CpuDfgMiner = CpuDfgMiner(computing_node.cpu)
        self.storage: StorageDfgMiner = StorageDfgMiner(computing_node.memory)
        network_access = computing_topology.get_labeled_network_for_computing_node("sensor", computing_node.get_name())
        self.network: NetworkAccessDfgMiner = NetworkAccessDfgMiner(node_id, computing_node.network, network_access)

    def get_latest_event_with_case_id(self, case_id) -> Event | None:
        return self.storage.get_latest_event_with_case_id(case_id)

    def receive_event(self, incoming_event: Event):
        local_preceding_event = self.storage.get_latest_event_with_case_id(incoming_event.caseid)
        self.storage.store_event(incoming_event)

        potential_preceding_events = self.network.get_latest_event_with_case_id(incoming_event.caseid)
        if local_preceding_event:
            potential_preceding_events.append(local_preceding_event)

        if potential_preceding_events:
            predecessor = self.cpu.compute_largest_timestamp(potential_preceding_events).activity
        else:
            predecessor = "<start>"

        self.storage.store_directly_follows_relation(DirectlyFollowsRelation(predecessor, incoming_event.activity))

    def get_directly_follows_graph(self) -> DirectlyFollowsGraph:
        directly_follows_relations: Dict[
            DirectlyFollowsRelation, int] = self.storage.get_all_directly_follows_relations()
        counted_relations: Dict[tuple[Any, Any], int] = dict()
        for dfr in directly_follows_relations:
            counted_relations[dfr.to_pair()] = directly_follows_relations[dfr]

        return DirectlyFollowsGraph(counted_relations, [], [])

    def get_directly_follows_graph_request(self) -> DirectlyFollowsGraph:
        results = self.network.get_directly_follows_graph()
        return self.merge_sub_dfgs(results)

    def merge_sub_dfgs(self, directly_follows_graphs: List[DirectlyFollowsGraph]):
        if not directly_follows_graphs:
            return None
        resulting_directly_follows_graph = directly_follows_graphs[0]
        for dfg in directly_follows_graphs:
            resulting_directly_follows_graph = self.cpu.merge_dfgs(resulting_directly_follows_graph, dfg)
        return resulting_directly_follows_graph