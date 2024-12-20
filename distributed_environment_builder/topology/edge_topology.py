from distributed_environment_builder.infrastructure.network_dfg_miner import Network
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology

class EdgeTopology:

    def __init__(self, node_count, ):
        self.node_count = node_count

    def get_infrastructure(self, node_constructor):
        computing_topology = ComputingTopology()
        network = Network("sensor")
        computing_topology.add_network("net", network)

        for i in range(self.node_count):
            node_id = f"sensor-{i}"
            computing_topology.add_computing_node(
                name=node_id,
                computing_node=node_constructor(node_id),
                network_ids=["net"]
            )

        return computing_topology