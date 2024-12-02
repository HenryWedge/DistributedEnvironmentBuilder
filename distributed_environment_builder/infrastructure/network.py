from abc import ABC

class Network(ABC):

    def add_node(self, node_id, node):
        pass

    def get_node(self, node_id: str):
        pass

    def get_all_node_ids(self):
        pass

    def get_all_nodes(self, own_node_id):
        pass
