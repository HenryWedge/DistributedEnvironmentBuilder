from typing import Dict, List
from distributed_environment_builder.algo.dfgminer.dfg_miner_abstract import AbstractDfgMiner

class Network:

    def __init__(self, label):
        self.nodes: Dict[str, AbstractDfgMiner] = dict()
        self._label = label

    def add_node(self, node_id: str, node: AbstractDfgMiner):
        self.nodes[node_id] = node

    def get_node(self, node_id: str):
        return self.nodes[node_id]

    def get_all_nodes(self, own_node_id):
        all_nodes: List[AbstractDfgMiner] = []
        for node in self.nodes:
            #  TODO remove this HACK!
            if node != own_node_id and "intermediary" not in node:
                all_nodes.append(self.nodes[node])
        return all_nodes

    def get_all_nodes_intermediary(self, own_node_id):
        all_nodes: List[AbstractDfgMiner] = []
        for node in self.nodes:
            if node != own_node_id:
                all_nodes.append(self.nodes[node])
        return all_nodes

    def get_all_node_ids(self):
        result = []
        for node_id in self.nodes:
            result.append(node_id)
        return result

    def get_label(self):
        return self._label
