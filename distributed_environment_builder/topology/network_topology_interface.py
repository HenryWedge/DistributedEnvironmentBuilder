from typing import List

from distributed_environment_builder.algo.baseline.interface.central_node_interface import CentralNodeInterface
from distributed_environment_builder.algo.baseline.interface.edge_node_interface import EdgeNodeInterface

class NetworkTopology:

    def add_connection(self, sender_node, receiving_node_id, cost):
        pass

    def add_constant_connection_cost(self, sender_id, cost):
        pass

    def add_edge_participant(self, participant):
        pass

    def add_central_participant(self, participant):
        pass

    def get_all_nodes(self):
        pass

    def broadcast(self, sender_id) -> List[EdgeNodeInterface]:
        pass

    def send_edge_nodes(self, sender_id) -> List[EdgeNodeInterface]:
        pass

    def send_central_nodes(self, sender_id) -> List[CentralNodeInterface]:
        pass

    def get_used_bandwidth(self):
        pass
