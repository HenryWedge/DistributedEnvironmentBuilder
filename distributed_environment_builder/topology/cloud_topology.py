from distributed_environment_builder.algo.dfgminer.hardware.network_dfg_miner import Network
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology

class CloudTopology:

    def __init__(self, node_count):
        self.node_count = node_count

    def get_infrastructure(self, edge_node, cloud_node):
        computing_topology = ComputingTopology()
        network_ids = []

        for i in range(self.node_count):
            network = Network("cloud")
            computing_topology.add_network(f"link-{i}", network)
            network_ids.append(f"link-{i}")

            node_id=f"sensor-{i}"
            computing_topology.add_computing_node(
                name=node_id,
                computing_node=edge_node(node_id),
                network_ids=[f"link-{i}"]
            )

        #network = Network("cloud")
        #computing_topology.add_network("cloud", network)
        #network_ids.append("cloud")
        node_id="cloud"
        computing_topology.add_computing_node(
            node_id,
            computing_node=cloud_node(node_id),
            network_ids=network_ids
        )

        return computing_topology