from typing import Dict, List

from distributed_environment_builder.algo.edgemine.edge_miner_abstract import AbstractEdgeMiner

class EdgeMineTopology:

    def __init__(self):
        self.nodes: Dict[str, AbstractEdgeMiner] = dict()

    def add_node(self, node_id: str, node: AbstractEdgeMiner):
        self.nodes[node_id] = node

    def get_node(self, node_id: str):
        return self.nodes[node_id]

    def get_all_node_ids(self):
        result = []
        for node_id in self.nodes:
            result.append(node_id)
        return result

    def get_all_nodes(self, own_node_id):
        all_nodes: List[AbstractEdgeMiner] = []
        for node in self.nodes:
            if node != own_node_id:
                all_nodes.append(self.nodes[node])
        return all_nodes
