from typing import List

from distributed_environment_builder.algo.edgemine.hardware.cpu_edge_mine import EdgeMineCpu
from distributed_environment_builder.algo.edgemine.hardware.network_access_edge_mine import EdgeMineNetwork
from distributed_environment_builder.algo.edgemine.hardware.storage_edge_mine import EdgeMineStorage
from distributed_environment_builder.benchmark.abstract_algorithm import Algorithm
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology
from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph


class EdgeDfgMiner(Algorithm):

    def __init__(self):

        super().__init__(["sensor"])
        self.storage = None
        self.network = None
        self.cpu: EdgeMineCpu = None
        self.node_id = None

    def assign_to_node(
            self,
            node_id,
            computing_topology: ComputingTopology,
        ):
        self.node_id = node_id
        computing_node= computing_topology.get_computing_node(node_id)
        topology = computing_topology.get_network_for_computing_node(node_id)[0]
        self.cpu: EdgeMineCpu = EdgeMineCpu(computing_node.cpu)
        self.network: EdgeMineNetwork = EdgeMineNetwork(node_id, topology, computing_node.network)
        self.storage: EdgeMineStorage = EdgeMineStorage(computing_node.memory)
        self.setup_most_frequent_predecessors()

    def setup_most_frequent_predecessors(self):
        for node_id in self.network.get_all_node_ids():
            if node_id != self.node_id:
                self.storage.store_predecessor(node_id)

    def receive_event(self, event: Event):
        self.setup_most_frequent_predecessors()
        self.storage.store_latest_event_for_case_id(event.caseid, event)
        preceding_event, node_id = self._get_all_events_from_others(event.caseid)
        if preceding_event:
            self.storage.store_predecessor(preceding_event.node)
            self.storage.store_directly_follows_relation(DirectlyFollowsRelation(preceding_event.activity, event.activity))
            self.network.inform_predecessor(event.caseid, node_id, event.activity)
        else:
            self.storage.store_directly_follows_relation(DirectlyFollowsRelation("<start>", event.activity))

    def _get_all_events_from_others(self, case_id):
        event = None
        node_id = None
        for node_id in self.storage.get_most_frequent_predecessors():
            event = self.network.get_latest_activity_with_case_id_mfp(case_id, node_id)
            if event:
                break
        return event, node_id

    def get_latest_activity_with_case_id(self, case_id):
        return self.storage.get_latest_event_for_case(case_id)

    def get_directly_follows_graph(self):
        return self.storage.get_directly_follows_relations()

    def get_directly_follows_graph_request(self):
        return self.merge_sub_dfgs(self.network.get_directly_follows_graph())

    def merge_sub_dfgs(self, directly_follows_graphs: List[DirectlyFollowsGraph]):
        if not directly_follows_graphs:
            return None
        resulting_directly_follows_graph = directly_follows_graphs[0]
        for dfg in directly_follows_graphs:
            resulting_directly_follows_graph = self.cpu.merge_dfgs(dfg, resulting_directly_follows_graph)
        return resulting_directly_follows_graph

    def inform_predecessor(self, case_id, node_id, activity):
        self.storage.store_case_successor(case_id, node_id)
        preceding_event = self.storage.get_latest_event_for_case(case_id)
        self.storage.store_directly_follows_relation(DirectlyFollowsRelation(preceding_event.activity, activity))
