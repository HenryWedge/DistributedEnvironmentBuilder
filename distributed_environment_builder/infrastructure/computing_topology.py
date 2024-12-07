from typing import Dict, List
from distributed_environment_builder.algo.dfgminer.hardware.network_dfg_miner import Network
from distributed_environment_builder.infrastructure.computing_node import ComputingNode


class ComputingTopology:

    def __init__(
            self,
            computing_nodes=None,
            networks=None
    ):
        if computing_nodes is None:
            computing_nodes = dict()
        if networks is None:
            networks = dict()
        self.computing_nodes: Dict[str, ComputingNode] = computing_nodes
        self.networks: Dict[str, Network] = networks
        self.node_network_mapping: Dict[str, List[str]] = dict()

    def add_computing_node(self, name, computing_node: ComputingNode, network_ids: List[str]):
        self.computing_nodes[name] = computing_node
        if name in self.node_network_mapping:
            self.node_network_mapping[name].extend(network_ids)
        else:
            self.node_network_mapping[name] = network_ids

    def add_network(self, name, network: Network):
        self.networks[name] = network

    def get_network_for_computing_node(self, computing_node_id: str) -> List[Network]:
        result = []
        networks = self.node_network_mapping[computing_node_id]
        for network in networks:
            result.append(self.networks[network])
        return result

    def get_labeled_network_for_computing_node(self, label: str, computing_node_id: str) -> Network:
        networks = self.get_network_for_computing_node(computing_node_id)
        for network in networks:
            if network.get_label() == label:
                return network

    def get_labeled_network_list_for_computing_node(self, label: str, computing_node_id: str) -> List[Network]:
        return [network for network in self.get_network_for_computing_node(computing_node_id) if
                network.get_label() == label]

    def get_nodes_with_label(self, label: str):
        result = []
        for key in self.computing_nodes:
            computing_node = self.computing_nodes[key]
            if computing_node.get_label() == label:
                result.append(computing_node)
        return result

    def get_computing_node(self, name: str) -> ComputingNode:
        return self.computing_nodes[name]

    def get_cpus(self):
        result = dict()
        for computing_node in self.computing_nodes:
            result[f"cpu-{computing_node}"] = self.computing_nodes[computing_node].cpu
        return result

    def get_memories(self):
        result = dict()
        for computing_node in self.computing_nodes:
            result[f"mem-{computing_node}"] = self.computing_nodes[computing_node].memory
        return result

    def get_networks(self):
        result = dict()
        for computing_node in self.computing_nodes:
            result[f"net-{computing_node}"] = self.computing_nodes[computing_node].network
        return result

    def get_networks_with_label(self, label):
        result = dict()
        for computing_node in self.computing_nodes:
            if self.computing_nodes[computing_node].get_label() == label:
                result[f"net-{computing_node}"] = self.computing_nodes[computing_node].network
        return result

    def increase_network_capacities(self, new_capacity, label):
        networks = self.get_networks_with_label(label)
        for network in networks:
            networks[network].adjust_capacity(new_capacity)

    def reset(self):
        for node in self.computing_nodes:
            self.computing_nodes[node].reset()
