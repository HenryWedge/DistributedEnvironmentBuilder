from typing import Dict, List

from distributed_environment_builder.benchmark.abstract_algorithm import Algorithm

class Network[T: Algorithm]:

    def __init__(self, label):
        self.nodes: Dict[str, T] = dict()
        self._label = label

    def get_label(self) -> str:
        return self._label

    def get_node(self, node_id: str) -> T:
        return self.nodes[node_id]

    def add_node(self, node_id: str, node: T) -> None:
        self.nodes[node_id] = node

    def get_all_nodes_with_protocol(self, own_node_id: str, protocol_label: str) -> List[T]:
        return [node for key, node in self.nodes.items() if key != own_node_id and protocol_label in node.get_protocol_ids()]

    def get_all_node_ids(self) -> List[str]:
        result = []
        for node_id in self.nodes:
            result.append(node_id)
        return result
