import sys

from hello_algorithm import SayHelloAlgorithm
from topology_factory import TopologyFactory

def parse_topology(file):
    return TopologyFactory(file).parse()

def run(topology, node_id):
    topology.deploy(SayHelloAlgorithm(), "node1")
    topology.deploy(SayHelloAlgorithm(), "node2")
    topology.run(node_id)

def run_mock(node_id):
    topology = parse_topology("topology-mock.yaml")
    run(topology, node_id=node_id)
    topology.get_node("node1").network.send_message("node2", "hi", dict())
    topology.get_node("node1").network.send_message("node2", "hello", {"message": "Max"})

def run_http(node_id):
    topology = parse_topology("topology-http.yaml")
    run(topology, node_id)

if __name__ == '__main__':
    #run_http(sys.argv[1])
    run_mock(sys.argv[1])