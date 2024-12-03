from distributed_environment_builder.algo.dfgminer.hardware.network_dfg_miner import Network
from distributed_environment_builder.infrastructure.hii.cpu_hii import CpuInstruction
from distributed_environment_builder.infrastructure.hii.network_hii import NetworkInstruction
from distributed_environment_builder.infrastructure.hii.storage_hii import StorageInstruction
from distributed_environment_builder.infrastructure.computing_node import ComputingNode
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology

class EdgeTopology:

    def __init__(self, node_count):
        self.node_count = node_count

    def get_infrastructure(self):
        computing_topology = ComputingTopology()
        network = Network("sensor")
        computing_topology.add_network("net", network)

        for i in range(self.node_count):
            cpu = CpuInstruction(lambda p: p, lambda p: p, 10)
            storage_write = StorageInstruction(lambda p: p, lambda p: p, 1000)
            network_send = NetworkInstruction(lambda p: p, lambda p: p, 10)

            computing_topology.add_computing_node(
                name=f"sensor-{i}",
                computing_node=ComputingNode(
                    name=f"sensor-{i}",
                    label="sensor",
                    cpu=cpu,
                    memory=storage_write,
                    network=network_send
                ),
                network_ids=["net"]
            )

        return computing_topology