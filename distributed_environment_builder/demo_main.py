import os

import yaml
from distributed_environment_builder.algo.dfgminer.dfg_miner import DfgMiner
from distributed_environment_builder.algo.edgemine.edge_miner import EdgeDfgMiner
from distributed_environment_builder.benchmark.algo_sink import DfgMinerAlgoSink
from distributed_environment_builder.benchmark.benchmark import Benchmark
from distributed_environment_builder.benchmark.def_event_emitter import DefEventEmitter
from distributed_environment_builder.benchmark.deployed_algorithm import DeployedAlgorithm
from distributed_environment_builder.benchmark.distributed_algorithm import DistributedAlgorithm
from distributed_environment_builder.graph_visualizer.graph_visualizer import GraphVisualizer
from distributed_environment_builder.topology.edge_topology import EdgeTopology
from distributed_event_factory.core.datasource_id import END_DATA_SOURCE
from distributed_event_factory.core.end_datasource import EndDataSource
from distributed_event_factory.event_factory import EventFactory
from distributed_environment_builder.nodes import edge_node
from distributed_event_factory.provider.data.constant_count_provider import ConstantCountProvider
from distributed_event_factory.provider.data.increasing_case import IncreasingCaseIdProvider
from distributed_event_factory.simulation.process_simulation import DefProcessSimulator

def demo_run():
    datasources = [
        "GoodsDelivery",
        "MaterialPreparation",
        "AssemblyLineSetup",
        "Assembling",
        "QualityControl",
        "Packaging",
        "Shipping",
    ]

    deployed_algorithm = DeployedAlgorithm(edge_topology(), edge_miner).deploy()

    for i, node_id in enumerate(datasources):
        event_factory.add_sink(
            f"sensor-{i}",
            DfgMinerAlgoSink(
                data_source_ref=[node_id],
                miner=deployed_algorithm.get_algorithm(f"sensor-{i}")
            )
        )
    event_factory.run(lambda: print(deployed_algorithm.get_algorithm("sensor-0").get_directly_follows_graph_request()))

def demo_benchmarks(event_emitter):
    benchmarks = [
        Benchmark(event_emitter, edge_topology, edge_miner, "sensor-0"),
        Benchmark(event_emitter, edge_topology, dfg_miner_edge, "sensor-0")
    ]
    benchmark_results = []

    for benchmark in benchmarks:
        benchmark.check_slo(50, 200)
        monitor = benchmark.monitor
        benchmark_results.append(monitor.cpu_utilization_timeseries)

    GraphVisualizer().view(
        "CPU Utilization",
        benchmark_results
    )


if __name__ == '__main__':
    event_factory: EventFactory = (
        EventFactory()
        .add_directory(directory="../config/assemblyline")
        .add_file(filename="../config/countbased.yaml")
    )

    datasources = dict()
    datasources[END_DATA_SOURCE] = EndDataSource()
    parser = event_factory.parser.datasource_parser
    for filename in os.listdir("../config/assemblyline"):
        with open("../config/assemblyline/"+ filename) as file:
            config = yaml.safe_load(file)
            datasources[config["name"]] = parser.parse(config["spec"])

    process_simulator = DefProcessSimulator(
        data_sources=datasources,
        case_id_provider=IncreasingCaseIdProvider(),
        max_concurrent_cases=ConstantCountProvider(1)
    )

    event_emitter = DefEventEmitter(process_simulator)
    edge_topology = lambda: EdgeTopology(7).get_infrastructure(edge_node)

    edge_miner = DistributedAlgorithm().add_algorithm("sensor", lambda: EdgeDfgMiner())
    dfg_miner_edge = DistributedAlgorithm().add_algorithm("sensor", lambda: DfgMiner())

    demo_run()
    #demo_benchmarks(event_emitter)