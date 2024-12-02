from distributed_environment_builder.algo.dfgminer.dfg_miner import DfgMiner
from distributed_environment_builder.algo.dfgminer.dfg_miner_intermediary import DfgMinerIntermediary
from distributed_environment_builder.algo.edgemine.edge_miner import EdgeDfgMiner
from distributed_environment_builder.platform.monitoring import TopologyMonitor
from distributed_environment_builder.topology.edge_topology import EdgeTopology
from distributed_environment_builder.topology.fog_topology import FogTopology
from distributed_environment_builder.platform.algo_sink import DfgMinerAlgoSink
from distributed_environment_builder.platform.distributed_algorithm import DistributedAlgorithm
from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':
    is_improved = True
    is_sourced = True
    event_factory: EventFactory = (
        EventFactory()
        .add_directory(directory="../../../DistributedEventFactory/config/datasource/assemblyline")
        .add_file(filename="../../../DistributedEventFactory/config/simulation/countbased.yaml"))

    datasources = [
        "GoodsDelivery",
        "MaterialPreparation",
        "AssemblyLineSetup",
        "Assembling",
        "QualityControl",
        "Packaging",
        "Shipping",
    ]

    intermediary_node_count = 0
    if is_sourced:
        computing_topology = EdgeTopology(len(datasources)).get_infrastructure()
    else:
        intermediary_node_count = 3
        computing_topology = FogTopology(len(datasources), intermediary_node_count).get_infrastructure()

    distributed_algorithm = DistributedAlgorithm(computing_topology)
    monitor = TopologyMonitor(computing_topology)

    for i, computing_node in enumerate(computing_topology.get_nodes_with_label("intermediary")):
        distributed_algorithm.add_algorithm(f"intermediary-{i}", computing_node.get_name(), DfgMinerIntermediary())

    for i, node_id in enumerate(datasources):
        generic_node_id = f"sensor-{i}"
        if is_improved:
            algorithm = EdgeDfgMiner()
        else:
            algorithm = DfgMiner()

        distributed_algorithm.add_algorithm(generic_node_id, generic_node_id, algorithm)
        event_factory.add_sink(generic_node_id, DfgMinerAlgoSink(data_source_ref=[node_id], miner=algorithm))

    event_factory.run(
        hook=lambda: (
            print(distributed_algorithm.get_algorithm("sensor-0").get_directly_follows_graph_request()),
            monitor.update(1, 0.05),
            print("Utilization:", monitor.average_utilization()),
            print("Processing Time:", monitor.average_processing_time())
        )
    )
