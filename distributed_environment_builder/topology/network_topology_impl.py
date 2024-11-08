from typing import Dict, List

from distributed_environment_builder.algo.baseline.impl.centralnode import CentralNode
from distributed_environment_builder.algo.baseline.interface.central_node_interface import CentralNodeInterface
from distributed_environment_builder.algo.baseline.interface.edge_node_interface import EdgeNodeInterface
from distributed_environment_builder.topology.network_topology_interface import NetworkTopology
from distributed_environment_builder.hardware.network import Network
from distributed_environment_builder.algo.baseline.impl.edgenode import EdgeNode

class NetworkTopologyImpl(NetworkTopology, Network):

    def __init__(self):
        self.edge_nodes: Dict[str, EdgeNode] = dict()
        self.central_nodes: Dict[str, CentralNode] = dict()
        self.connections: Dict[tuple[str, str], int] = dict()
        self.used_bandwidth = 0

    def add_connection(self, sender_node, receiving_node_id, cost):
        self.connections[sender_node, receiving_node_id] = cost

    def add_constant_connection_cost(self, sender_id, cost):
        for receiver_id in self.get_all_nodes():
            if receiver_id != sender_id:
                self.add_connection(sender_id, receiver_id, cost)

    def add_edge_participant(self, participant: EdgeNode):
        self.edge_nodes[participant.sender_id] = participant

    def add_central_participant(self, participant: CentralNode):
        self.central_nodes[participant.sender_id] = participant

    def get_all_nodes(self):
        all_nodes = []
        for key in self.edge_nodes:
            all_nodes.append(key)
        for key in self.central_nodes:
            all_nodes.append(key)
        return all_nodes

    def send_edge_node(self, sender_id, receiving_id) -> EdgeNodeInterface:
        self.get_connection_cost(receiving_id, sender_id)
        return self.edge_nodes[receiving_id]

    def send_edge_nodes(self, sender_id) -> List[EdgeNodeInterface]:
       edge_nodes = []
       for receiver_id in self.edge_nodes:
           if receiver_id != sender_id:
               self.get_connection_cost(receiver_id, sender_id)
               edge_nodes.append(self.edge_nodes[receiver_id])
       return edge_nodes

    def send_central_nodes(self, sender_id) -> List[CentralNodeInterface]:
        central_nodes = []
        for receiver_id in self.central_nodes:
            if receiver_id != sender_id:
                self.get_connection_cost(receiver_id, sender_id)
                central_nodes.append(self.central_nodes[receiver_id])
        return central_nodes

    def get_connection_cost(self, receiving_id, sender_id):
        if (sender_id, receiving_id) in self.connections:
            self.used_bandwidth += self.connections[(sender_id, receiving_id)]
        else:
            self.used_bandwidth += self.connections[(receiving_id, sender_id)]

    def get_used_bandwidth(self):
        return self.used_bandwidth

