import yaml

from compute.mock.mock_compute import MockConstantCompute
from hello_node import HelloNode
from hello_topology import HelloTopology
from network.fw.http_network import HttpNetwork
from network.fw.mock_network import MockNetwork
from node_monitor import NodeMonitor
from storage.dict_storage import DictStorage
from storage.file_storage import DictFileStorage
from topology_monitor import TopologyMonitor


class TopologyFactory:
    def __init__(self, filename, topology_monitor):
        self.topology_monitor: TopologyMonitor = topology_monitor
        with open(filename) as file:
            config = yaml.safe_load(file)
            self.topology: HelloTopology = HelloTopology()
            self.nodes = config["nodes"]

    def parse(self) -> HelloTopology:
        for node in self.nodes:
            datasources = node["label"]["datasources"]
            name = node["name"]
            if node["type"] == "mock":
                new_node = HelloNode(
                    node_id=name,
                    data_network=MockNetwork(
                        network_router=self.topology.network_address_resolution,
                        initial_time=0.01,
                        initial_resource=0.02,
                        throughput=200,
                        payload=1
                    ),
                    control_network=MockNetwork(
                        network_router=self.topology.network_address_resolution,
                        initial_time=0.01,
                        initial_resource=0.02,
                        throughput=200,
                        payload=1
                    ),
                    compute_generator=lambda name: MockConstantCompute(
                        initial_time=0.01,
                        initial_resource=0.02,
                        throughput=100,
                        payload=2
                    ),
                    storage_generator=lambda name: DictStorage(
                        initial_time=0.01,
                        initial_resource=0.02,
                        throughput=100,
                        payload=2
                    ),
                    category=node["label"]["category"],
                    datasources=datasources,
                    monitor=self.topology_monitor.add_node(name)
                )
                self.topology.add_node(
                    name,
                    new_node
                )
            else:
                port = node["port"]
                new_node = HelloNode(
                    name,
                    HttpNetwork(self.topology.network_address_resolution, port),
                    lambda name: DictFileStorage(name),
                    node["label"]["category"],
                    datasources,
                    NodeMonitor()
                )
                self.topology.add_node(
                    datasources,
                    new_node
                )
        return self.topology