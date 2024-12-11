from typing import Dict, Any

from distributed_environment_builder.benchmark.abstract_algorithm import Algorithm
from distributed_environment_builder.benchmark.distributed_algorithm import DistributedAlgorithm
from distributed_environment_builder.infrastructure.computing_node import ComputingNode
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology

class DeployedAlgorithm:

    def __init__(self, computing_topology: ComputingTopology, distributed_algorithm: DistributedAlgorithm):
        self._computing_topology: ComputingTopology = computing_topology
        self._distributed_algorithm: DistributedAlgorithm = distributed_algorithm
        self._algorithm_nodes: Dict[str, Algorithm] = dict()

    def receive(self):
        pass

    def request(self):
        pass

    def deploy(self):
        for computing_node in self._computing_topology.computing_nodes:
            node: ComputingNode = self._computing_topology.computing_nodes[computing_node]
            self.add_algorithm(node.get_name(), self._distributed_algorithm.create_algorithm_of_key(node.get_label()))
        return self

    def add_algorithm(self, computing_node_id, algorithm: Algorithm):
        network_topologies = self._computing_topology.get_network_for_computing_node(computing_node_id)

        for network_topology in network_topologies:
            network_topology.add_node(computing_node_id, algorithm)

        algorithm.assign_to_node(
            node_id=computing_node_id,
            computing_topology=self._computing_topology
        )
        self._algorithm_nodes[computing_node_id] = algorithm

    def get_algorithm(self, algorithm_node_id):
        return self._algorithm_nodes[algorithm_node_id]
