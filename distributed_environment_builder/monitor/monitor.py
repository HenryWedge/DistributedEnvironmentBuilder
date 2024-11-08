from DistributedEnvironmentBuilder.distributed_environment_builder.topology.topology import Topology


class Monitor:

    def __init__(self, topology: Topology):
        self.topology: Topology = topology

    def get_network_cost(self) -> int:
        network_cost = 0
        for node in self.topology.nodes:
            network_cost += node.storage.get_size_stored_objects()
        return network_cost

    def get_time_cost(self) -> int:
        network_cost = 0
        for node in self.topology.nodes:
            network_cost += node.storage.get_size_stored_objects()
        return network_cost

    def get_storage_cost(self) -> int:
        network_cost = 0
        for node in self.topology.nodes:
            network_cost += node.storage.get_size_stored_objects()
        return network_cost