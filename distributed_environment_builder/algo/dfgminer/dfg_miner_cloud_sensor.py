from distributed_environment_builder.algo.dfgminer.hardware.network_access_dfg_miner_cloud_sensor import \
    NetworkAccessDfgMinerCloudSensor
from distributed_environment_builder.benchmark.abstract_algorithm import Algorithm
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology
from process_mining_core.datastructure.core.event import Event


class DfgMinerCloudSensor(Algorithm):
    def __init__(
            self
    ):
        super().__init__(["sensor"])
        self.network: NetworkAccessDfgMinerCloudSensor = None
        self.storage = None
        self.cpu = None

    def assign_to_node(
            self,
            node_id,
            computing_topology: ComputingTopology):
        computing_node = computing_topology.get_computing_node(node_id)
        network_access = computing_topology.get_labeled_network_for_computing_node("cloud", computing_node.get_name())
        self.network: NetworkAccessDfgMinerCloudSensor = NetworkAccessDfgMinerCloudSensor(node_id, computing_node.network, network_access)

    def receive_event(self, incoming_event: Event):
        self.network.send_event(incoming_event)