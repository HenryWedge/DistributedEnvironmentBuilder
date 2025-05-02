import yaml

from hello_network import HelloNetwork
from hello_topology import HelloTopology
from network.fw.http_network import HttpNetwork
from network.fw.mock_network import MockNetwork
from nodes.hello_node import HelloNode
from nodes.mock_hello_node import MockHelloNode
from storage.mock_hello_storage import ListStorage


class TopologyFactory:

    def __init__(self, filename):
        with open(filename) as file:
            config = yaml.safe_load(file)
            self.topology = HelloTopology()
            self.nodes = config["nodes"]
            self.network_address_resolution = HelloNetwork()

    def start_nodes(self):
        for node in self.nodes:
            if node["type"] == "mock":
                node_name = node["name"]
                new_node = MockHelloNode(
                    node_name,
                    MockNetwork(self.network_address_resolution),
                    ListStorage()
                )
                self.topology.add_node(
                    node["name"],
                    new_node
                )
                self.network_address_resolution.add_network_address(node_name, new_node)
            else:
                node_name = node["name"]
                port = node["port"]
                new_node = HelloNode(
                        "node1",
                        port,
                        HttpNetwork(self.network_address_resolution),
                        ListStorage()
                    )
                self.topology.add_node(
                    node_name,
                    new_node
                )
                self.network_address_resolution.add_network_address(node_name, f"localhost:{port}")