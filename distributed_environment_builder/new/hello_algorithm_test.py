import os

from hello_algorithm import SayHelloAlgorithm
from hello_network import HelloNetwork
from hello_topology import HelloTopology
from network.http_network_function import HttpNetworkFunction
from new_network import NewNetwork
from nodes.hello_node import HelloNode
from storage.mock_hello_storage import ListStorage

if __name__ == '__main__':
    topology = HelloTopology()

    #network = HelloNetwork()
    network = NewNetwork()
    network.add_network_function("hi", HttpNetworkFunction(None, "hello", "POST", None))
    network.add_network_function("hello", HttpNetworkFunction(None, "hello", "POST", None))
    storage = ListStorage()

    topology.add_network("net1", network)
    node  = HelloNode(8082, network, storage)
    node2 = HelloNode(8084, network, storage)

    topology.add_node("node1", node)
    topology.add_node("node2", node2)

    topology.run(SayHelloAlgorithm(), "node1")
