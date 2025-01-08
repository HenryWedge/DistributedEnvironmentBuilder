from distributed_environment_builder.infrastructure.computing_node import ComputingNode
from distributed_environment_builder.infrastructure.hii.cpu_hii import CpuInstruction
from distributed_environment_builder.infrastructure.hii.network_hii import NetworkInstruction
from distributed_environment_builder.infrastructure.hii.storage_hii import StorageInstruction

edge_node = lambda name: ComputingNode(
        name,
        "sensor",
        cpu=CpuInstruction(lambda p: 2 * p, lambda p: p, 100),
        memory=StorageInstruction(lambda p: 2 * p, lambda p: p, 100),
        network=NetworkInstruction(lambda p: p, lambda p: p, 100)
    )

edge_node_2 = lambda name: ComputingNode(
    name,
    "sensor",
    cpu=CpuInstruction(lambda p: 2 * p, lambda p: p, 100),
    memory=StorageInstruction(lambda p: 2 * p, lambda p: p, 100),
    network=NetworkInstruction(lambda p: 5 * p, lambda p: p, 100)
)

fog_node = lambda name: ComputingNode(
    name,
    "intermediary",
    cpu=CpuInstruction(lambda p: 1.5 * p, lambda p: p, 150),
    memory=StorageInstruction(lambda p: 1.5 * p, lambda p: p, 150),
    network=NetworkInstruction(lambda p: 1.5 * p, lambda p: p, 150)
)

cloud_node = lambda name: ComputingNode(
    name,
    "cloud",
    cpu=CpuInstruction(lambda p: p, lambda p: p, 200),
    memory=StorageInstruction(lambda p: p, lambda p: p, 200),
    network=NetworkInstruction(lambda p: 1 * p, lambda p: p, 200)
)