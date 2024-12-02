from typing import Dict, Any

from distributed_environment_builder.platform.abstract_algorithm import AbstractAlgorithm
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology

class DistributedAlgorithm:

    def __init__(self, computing_topology: ComputingTopology):
        self._computing_topology = computing_topology
        self._algorithm_nodes: Dict[str, Any] = dict()

    def add_algorithm(self, algorithm_node_id, computing_node_id, algorithm: AbstractAlgorithm):
        network_topologies = self._computing_topology.get_network_for_computing_node(computing_node_id)
        for network_topology in network_topologies:
            network_topology.add_node(algorithm_node_id, algorithm)

        algorithm.assign_to_node(
            node_id=computing_node_id,
            computing_topology=self._computing_topology
        )
        self._algorithm_nodes[algorithm_node_id] = algorithm

    def get_algorithm(self, algorithm_node_id):
        return self._algorithm_nodes[algorithm_node_id]
