from distributed_environment_builder.algo.baseline.impl.cpu_edge_impl import CpuEdgeNode
from distributed_environment_builder.algo.baseline.impl.storage_edge_impl import StorageEdgeNode
from distributed_environment_builder.topology.network_topology_interface import NetworkTopology
from distributed_environment_builder.algo.baseline.impl.edgenode import EdgeNode
from distributed_environment_builder.topology.network_topology_registry import get_network_topology
from distributed_event_factory.provider.sink.sink_provider import Sink
from process_mining_core.datastructure.core.event import Event


class BaselineDfgMinerSink(Sink):
    def __init__(self, data_source_ref, sender_id, network_ref):
        super().__init__(data_source_ref)

        network_topology: NetworkTopology = get_network_topology(network_ref)
        self.processing_node = EdgeNode(
            sender_id=sender_id,
            cpu=CpuEdgeNode(instruction_cost=1),
            storage=StorageEdgeNode(storage_cost=1),
            network_topology=network_topology
        )

        network_topology.add_edge_participant(self.processing_node)
        network_topology.add_constant_connection_cost(sender_id, 1)

    def send(self, event: Event) -> None:
        self.processing_node.receive_event(event)

    def get_datasource_ref(self):
        return super().get_datasource_ref()