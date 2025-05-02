import sys

from hello_algorithm import SayHelloAlgorithm
from hello_network import HelloNetwork
from hello_topology import HelloTopology
from network.fw.http_network import HttpNetwork
from network.fw.mock_network import MockNetwork
from nodes.hello_node import HelloNode
from nodes.mock_hello_node import MockHelloNode
from storage.mock_hello_storage import ListStorage

if __name__ == '__main__':
    topology = HelloTopology()

    #network_access = MockNetwork()
    #network2_access = MockNetwork()

    network = HelloNetwork()
    network_access = HttpNetwork(network)
    network2_access = HttpNetwork(network)

    storage = ListStorage()
    network.add_network_access("node1", "localhost:8082", network_access)
    network.add_network_access("node2", "localhost:8084", network2_access)

    #node  = MockHelloNode(8082, network, network_access, storage)
    #node2 = MockHelloNode(8084, network, network2_access, storage)

    node  = HelloNode("node1", 8082, network, network_access, storage)
    node2 = HelloNode("node2", 8084, network, network2_access, storage)

    topology.add_node("node1", node)
    topology.add_node("node2", node2)

    #node.network.send_message("node1", "hi", dict())
    #node.network.send_message("node2", "hello", {"message": "Max"})

    topology.run(SayHelloAlgorithm(), "node1")
    topology.run(SayHelloAlgorithm(), "node2")

    topology.get_node(sys.argv[1]).run()
