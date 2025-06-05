import sys
from time import sleep

from conformance_visualizer import ConformanceViewer
from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.provider.data.constant_count_provider import ConstantCountProvider
from distributed_event_factory.provider.data.increasing_case import IncreasingCaseIdProvider
from distributed_event_factory.simulation.process_simulation import DefProcessSimulator
from hello_algorithm import SayHelloAlgorithm
from hello_topology import HelloTopology
from node_sink import NodeSink
from topology_factory import TopologyFactory
from topology_monitor import TopologyMonitor


def run_event_factory(topology):
    sleep(1)
    content_root = "../../../EventFactoryConfigs"
    event_factory = EventFactory()
    event_factory \
        .add_directory(f"{content_root}/datasource/assemblyline") \
        .add_file(f"{content_root}/simulation/countbased.yaml") \
        .add_process_simulator(DefProcessSimulator(dict(), IncreasingCaseIdProvider(), ConstantCountProvider(1)))
        #.add_process_simulator(XesProcessSimulator(f"{content_root}/Road_Traffic_Fine_Management_Process.xes"))

    sinks = []
    for node in topology.get_nodes():
        sink = NodeSink(node, node.datasources)
        sinks.append(sink)
        event_factory.add_sink(
            node.node_id,
            sink
        )
    event_factory.run(lambda i: topology.monitor(1, 100))

def parse_topology(file, topology_monitor):
    return TopologyFactory(file, topology_monitor).parse()

if __name__ == '__main__':
    algo = lambda: SayHelloAlgorithm()
    node_id = sys.argv[1]

    topology_monitor: TopologyMonitor = TopologyMonitor()
    topology: HelloTopology = parse_topology("topology/topology-mock.yaml", topology_monitor)
    topology.deploy_algorithm_on_nodes_with_category("edge", algo)
    topology.run_all()
    run_event_factory(topology)

    ConformanceViewer().show(topology_monitor.get_node_monitor("node1").metrics["compute-cpu-time"])
    ConformanceViewer().show(topology_monitor.get_node_monitor("node1").metrics["compute-cpu-resource"])

