import yaml

from hello_node import HelloNode
from hello_topology import HelloTopology
from network.fw.http_network import HttpNetwork
from network.fw.mock_network import MockNetwork
from storage.mock_hello_storage import ListStorage

class TopologyFactory:
    def __init__(self, filename):
        with open(filename) as file:
            config = yaml.safe_load(file)
            self.topology = HelloTopology()
            self.nodes = config["nodes"]

    def parse(self):
        for node in self.nodes:
            if node["type"] == "mock":
                node_name = node["name"]
                new_node = HelloNode(
                    node_name,
                    MockNetwork(self.topology.network_address_resolution, node["delay"]),
                    ListStorage()
                )
                self.topology.add_node(
                    node["name"],
                    new_node
                )
            else:
                node_name = node["name"]
                port = node["port"]
                new_node = HelloNode(
                    "node1",
                    HttpNetwork(self.topology.network_address_resolution, port),
                    ListStorage()
                )
                self.topology.add_node(
                    node_name,
                    new_node
                )
        return self.topology