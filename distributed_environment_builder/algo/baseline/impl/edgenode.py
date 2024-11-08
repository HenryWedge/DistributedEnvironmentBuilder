from typing import Dict, Any

from distributed_environment_builder.algo.baseline.interface.compute_interface import ComputeEdgeInterface
from distributed_environment_builder.algo.baseline.interface.edge_node_interface import EdgeNodeInterface
from distributed_environment_builder.algo.baseline.interface.store_interface import StorageEdgeInterface
from distributed_environment_builder.topology.network_topology_interface import NetworkTopology
from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph

class EdgeNode(EdgeNodeInterface):

    def __init__(
            self,
            sender_id: str,
            cpu: ComputeEdgeInterface,
            storage: StorageEdgeInterface,
            network_topology: NetworkTopology
    ):
        self.sender_id = sender_id
        self.cpu: ComputeEdgeInterface = cpu
        self.storage: StorageEdgeInterface = storage
        self.network_topology: NetworkTopology = network_topology

    def get_latest_event_with_case_id(self, case_id) -> Event | None:
        return self.storage.get_latest_event_with_case_id(case_id)

    def receive_event(self, incoming_event: Event):
        local_preceding_event = self.storage.get_latest_event_with_case_id(incoming_event.caseid)
        if local_preceding_event:
            potential_preceding_events = [local_preceding_event]
        else:
            potential_preceding_events = []

        self.storage.store_event(incoming_event)

        for edge_node in self.network_topology.send_edge_nodes(sender_id=self.sender_id):
            latest_event = edge_node.get_latest_event_with_case_id(incoming_event.caseid)
            if latest_event:
                potential_preceding_events.append(latest_event)

        if not potential_preceding_events:
            predecessor = "<start>"
        else:
            event = self.cpu.compute_largest_timestamp(potential_preceding_events)
            predecessor = event.activity

        self.storage.store_directly_follows_relation(
            DirectlyFollowsRelation(predecessor, incoming_event.activity)
        )

    def get_directly_follows_graph(self) -> DirectlyFollowsGraph:
        directly_follows_relations: Dict[DirectlyFollowsRelation, int] = self.storage.get_all_directly_follows_relations()
        counted_relations: Dict[tuple[Any,Any], int] = dict()
        start_activities = []
        for dfr in directly_follows_relations:
            if dfr.predecessor == "<start>":
                start_activities.append(dfr.successor)
            else:
                counted_relations[dfr.to_pair()] = directly_follows_relations[dfr]

        return DirectlyFollowsGraph(counted_relations, start_activities, [])
