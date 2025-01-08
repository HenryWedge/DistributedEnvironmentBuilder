from distributed_environment_builder.algo.dfgminer.dfg_miner import DfgMiner
from distributed_environment_builder.algo.dfgminer.dfg_miner_central import DfgMinerCentral
from distributed_environment_builder.algo.dfgminer.dfg_miner_cloud_sensor import DfgMinerCloudSensor
from distributed_environment_builder.algo.dfgminer.dfg_miner_intermediary import DfgMinerIntermediary
from distributed_environment_builder.algo.edgemine.edge_miner import EdgeDfgMiner
from distributed_environment_builder.benchmark.algo_sink import DfgMinerAlgoSink
from distributed_environment_builder.benchmark.benchmark import Benchmark
from distributed_environment_builder.benchmark.deployed_algorithm import DeployedAlgorithm
from distributed_environment_builder.benchmark.distributed_algorithm import DistributedAlgorithm
from distributed_environment_builder.experiment_runner import ExperimentRunner
from distributed_environment_builder.graph_visualizer.graph_visualizer import GraphVisualizer
from distributed_environment_builder.infrastructure.computing_node import ComputingNode
from distributed_environment_builder.infrastructure.hii.cpu_hii import CpuInstruction
from distributed_environment_builder.infrastructure.hii.network_hii import NetworkInstruction
from distributed_environment_builder.infrastructure.hii.storage_hii import StorageInstruction
from distributed_environment_builder.nodes import edge_node, edge_node_2, cloud_node, fog_node
from distributed_environment_builder.topology.cloud_topology import CloudTopology
from distributed_environment_builder.topology.edge_topology import EdgeTopology
from distributed_environment_builder.topology.fog_topology import FogTopology
from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':

    event_factory: EventFactory = (
        EventFactory()
        .add_directory(directory="../config/assemblyline")
        .add_file(filename="../config/countbased.yaml"))

    edge_topology = lambda: EdgeTopology(7).get_infrastructure(edge_node)
    fog_topology = lambda: FogTopology(7, 3).get_infrastructure(edge_node, fog_node)
    cloud_topology = lambda: CloudTopology(7).get_infrastructure(edge_node_2, cloud_node)

    edge_miner = DistributedAlgorithm().add_algorithm("sensor", lambda: EdgeDfgMiner())
    dfg_miner_edge = DistributedAlgorithm().add_algorithm("sensor", lambda: DfgMiner())

    dfg_miner_fog = (DistributedAlgorithm()
                     .add_algorithm("sensor", lambda: DfgMiner())
                     .add_algorithm("intermediary", lambda: DfgMinerIntermediary()))

    dfg_miner_cloud = (DistributedAlgorithm()
                       .add_algorithm("sensor", lambda: DfgMinerCloudSensor())
                       .add_algorithm("cloud", lambda: DfgMinerCentral()))

    #datasources = [
    #    "GoodsDelivery",
    #    "MaterialPreparation",
    #    "AssemblyLineSetup",
    #    "Assembling",
    #    "QualityControl",
    #    "Packaging",
    #    "Shipping",
    #]
#
    #deployed_algorithm = DeployedAlgorithm(edge_topology(), dfg_miner_edge).deploy()
#
    #for i, node_id in enumerate(datasources):
    #    event_factory.add_sink(
    #        f"sensor-{i}",
    #        DfgMinerAlgoSink(
    #            data_source_ref=[node_id],
    #            miner=deployed_algorithm.get_algorithm(f"sensor-{i}")
    #        )
    #    )
#
    #event_factory.run(lambda: print(deployed_algorithm.get_algorithm("sensor-0").get_directly_follows_graph_request()))

    benchmarks = [
        Benchmark(event_factory, edge_topology, edge_miner, "sensor-0"),
        Benchmark(event_factory, edge_topology, dfg_miner_edge, "sensor-0"),
        Benchmark(event_factory, fog_topology, dfg_miner_fog, "intermediary-0"),
        Benchmark(event_factory, cloud_topology, dfg_miner_cloud, "cloud"),
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
    experiment_runner = ExperimentRunner()
    #experiment_runner.run_scalability_test_load_capacity(benchmarks)
    #experiment_runner.run_scalability_test_resource_demand(benchmarks)
