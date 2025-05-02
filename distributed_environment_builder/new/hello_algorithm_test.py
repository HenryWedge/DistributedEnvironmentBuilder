import sys

from hello_algorithm import SayHelloAlgorithm
from topology_factory import TopologyFactory

if __name__ == '__main__':
    topology_factory = TopologyFactory("topology-mock.yaml")
    topology_factory.start_nodes()
    topology = topology_factory.topology

    topology.run(SayHelloAlgorithm(), "node1")
    topology.run(SayHelloAlgorithm(), "node2")

    topology.get_node("node1").network.send_message("node2", "hi", dict())
    topology.get_node("node1").network.send_message("node2", "hello", {"message": "Max"})

    #topology.get_node(sys.argv[1]).run()