from distributed_environment_builder.infrastructure.hii.cpu_hii import CpuInstruction
from distributed_environment_builder.infrastructure.hii.network_hii import NetworkInstruction
from distributed_environment_builder.infrastructure.hii.storage_hii import StorageInstruction


class ComputingNode:
    def __init__(
            self,
            name,
            label,
            cpu,
            memory,
            network
    ):
        self._name: str = name
        self._label: str = label
        self.cpu: CpuInstruction = cpu
        self.memory: StorageInstruction = memory
        self.network: NetworkInstruction = network

    def get_name(self):
        return self._name

    def get_label(self):
        return self._label