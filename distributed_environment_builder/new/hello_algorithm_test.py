import sys
from time import sleep

from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.provider.data.constant_count_provider import ConstantCountProvider
from distributed_event_factory.provider.data.increasing_case import IncreasingCaseIdProvider
from distributed_event_factory.simulation.process_simulation import DefProcessSimulator
from distributed_event_factory.simulation.xes_process_simulator import XesProcessSimulator
from hello_algorithm import SayHelloAlgorithm
from node_sink import NodeSink
from topology_factory import TopologyFactory


def run_event_factory(nodes):
    sleep(1)
    content_root = "../../../EventFactoryConfigs"
    event_factory = EventFactory()
    event_factory \
        .add_directory(f"{content_root}/datasource/assemblyline") \
        .add_file(f"{content_root}/simulation/countbased.yaml") \
        .add_process_simulator(DefProcessSimulator(dict(), IncreasingCaseIdProvider(), ConstantCountProvider(1)))
        #.add_process_simulator(XesProcessSimulator(f"{content_root}/Road_Traffic_Fine_Management_Process.xes"))

    for node in nodes:
        event_factory.add_sink(
            node.datasource,
            NodeSink(node, [node.datasource])
        )
    event_factory.run()


def parse_topology(file):
    return TopologyFactory(file).parse()

def run(topology, algo, node_id):
    topology.deploy(algo, "node0")
    topology.deploy(algo, "node1")
    topology.run(node_id)


if __name__ == '__main__':
    algo = lambda: SayHelloAlgorithm()
    node_id = sys.argv[1]
    topology = parse_topology("topology/topology-mock.yaml")
    topology.deploy_algorithm_on_nodes_with_category("edge", algo)
    topology.run_all()
    run_event_factory(topology.get_nodes())