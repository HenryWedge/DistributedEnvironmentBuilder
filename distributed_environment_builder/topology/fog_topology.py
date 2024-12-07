from distributed_environment_builder.algo.dfgminer.hardware.network_dfg_miner import Network
from distributed_environment_builder.infrastructure.hii.cpu_hii import CpuInstruction
from distributed_environment_builder.infrastructure.hii.network_hii import NetworkInstruction
from distributed_environment_builder.infrastructure.hii.storage_hii import StorageInstruction
from distributed_environment_builder.infrastructure.computing_node import ComputingNode
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology


class FogTopology:
    def __init__(self, source_node_count, intermediary_node_count):
        self.source_node_count = source_node_count
        self.intermediary_node_count = intermediary_node_count

    def get_infrastructure(self, edge_node, fog_node):
        computing_topology = ComputingTopology()

        for i in range(self.intermediary_node_count):
            computing_topology.add_network(f"net-{i}", Network(label="sensor"))
        computing_topology.add_network(f"net-{self.intermediary_node_count}", Network(label="intermediary"))

        for i in range(self.source_node_count):
            node_id = f"sensor-{i}"
            computing_topology.add_computing_node(
                name=node_id,
                computing_node=edge_node(node_id),
                network_ids=[f"net-{int(i / self.intermediary_node_count)}"]
            )

        for i in range(self.intermediary_node_count):
            node_id = f"intermediary-{i}"
            computing_topology.add_computing_node(
                name=node_id,
                computing_node=fog_node(node_id),
                network_ids=[f"net-{i}", f"net-{self.intermediary_node_count}"]
            )

        return computing_topology
