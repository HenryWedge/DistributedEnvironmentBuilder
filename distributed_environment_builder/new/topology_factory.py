import yaml

from hello_node import HelloNode
from hello_topology import HelloTopology
from network.fw.http_network import HttpNetwork
from network.fw.mock_network import MockNetwork
from storage.dict_storage import DictStorage

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
                    node["label"]["datasource"],
                    MockNetwork(self.topology.network_address_resolution, node["delay"]),
                    lambda: DictStorage(dictionary=dict()),
                    node["label"]["category"],
                    node["label"]["datasource"]
                )
                self.topology.add_node(
                    node["label"]["datasource"],
                    new_node
                )
            else:
                node_name = node["name"]
                port = node["port"]
                new_node = HelloNode(
                    "node1",
                    HttpNetwork(self.topology.network_address_resolution, port),
                    lambda: DictStorage(dict()),
                    node["label"]["category"],
                    node["label"]["datasource"]
                )
                self.topology.add_node(
                    node_name,
                    new_node
                )
        return self.topology