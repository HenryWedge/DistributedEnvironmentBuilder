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

    def get_infrastructure(self):
        computing_topology = ComputingTopology()

        for i in range(self.intermediary_node_count):
            computing_topology.add_network(f"net-{i}", Network(label="sensor"))
        computing_topology.add_network(f"net-{self.intermediary_node_count}", Network(label="intermediary"))

        for i in range(self.source_node_count):
            cpu = CpuInstruction(lambda p: p, lambda p: p)
            storage_write = StorageInstruction(lambda p: p, lambda p: p)
            network_send = NetworkInstruction(lambda p: p, lambda p: p)

            computing_topology.add_computing_node(
                name=f"sensor-{i}",
                computing_node=ComputingNode(
                    name=f"sensor-{i}",
                    label="sensor",
                    cpu=cpu,
                    memory=storage_write,
                    network=network_send
                ),
                network_ids=[f"net-{int(i/self.intermediary_node_count)}"]
            )

        for i in range(self.intermediary_node_count):
            cpu = CpuInstruction(lambda p: p, lambda p: p)
            storage_write = StorageInstruction(lambda p: p, lambda p: p)
            network_send = NetworkInstruction(lambda p: p, lambda p: p)

            computing_topology.add_computing_node(
                name=f"intermediary-{i}",
                computing_node=ComputingNode(
                    name=f"intermediary-{i}",
                    label="intermediary",
                    cpu=cpu,
                    memory=storage_write,
                    network=network_send
                ),
                network_ids=[f"net-{i}", f"net-{self.intermediary_node_count}"]
            )

        return computing_topology