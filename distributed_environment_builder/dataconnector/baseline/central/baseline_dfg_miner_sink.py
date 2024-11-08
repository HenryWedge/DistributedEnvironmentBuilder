from distributed_environment_builder.algo.baseline.impl.centralnode import CentralNode
from distributed_environment_builder.topology.network_topology_interface import NetworkTopology
from distributed_environment_builder.topology.network_topology_registry import get_network_topology
from distributed_event_factory.provider.sink.sink_provider import Sink
from process_mining_core.datastructure.core.event import Event

class BaselineDfgMinerCentralNode(Sink):
    def __init__(self, data_source_ref, sender_id, network_ref):
        super().__init__(data_source_ref)

        network_topology: NetworkTopology = get_network_topology(network_ref)
        self.processing_node: CentralNode = CentralNode(
            sender_id=sender_id,
            network_topology=network_topology
        )

        network_topology.add_central_participant(self.processing_node)
        network_topology.add_constant_connection_cost(sender_id, 1)

    def send(self, event: Event) -> None:
        pass

    def get_datasource_ref(self):
        return super().get_datasource_ref()