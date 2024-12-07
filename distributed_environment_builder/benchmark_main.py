from distributed_environment_builder.algo.dfgminer.dfg_miner import DfgMiner
from distributed_environment_builder.algo.dfgminer.dfg_miner_central import DfgMinerCentral
from distributed_environment_builder.algo.dfgminer.dfg_miner_cloud_sensor import DfgMinerCloudSensor
from distributed_environment_builder.algo.dfgminer.dfg_miner_intermediary import DfgMinerIntermediary
from distributed_environment_builder.algo.edgemine.edge_miner import EdgeDfgMiner
from distributed_environment_builder.benchmark.benchmark import Benchmark
from distributed_environment_builder.graph_visualizer.graph_visualizer import GraphVisualizer
from distributed_environment_builder.infrastructure.computing_node import ComputingNode
from distributed_environment_builder.infrastructure.hii.cpu_hii import CpuInstruction
from distributed_environment_builder.infrastructure.hii.network_hii import NetworkInstruction
from distributed_environment_builder.infrastructure.hii.storage_hii import StorageInstruction
from distributed_environment_builder.topology.cloud_topology import CloudTopology
from distributed_environment_builder.topology.edge_topology import EdgeTopology
from distributed_environment_builder.topology.fog_topology import FogTopology
from distributed_event_factory.event_factory import EventFactory

def run_multiple_benchmarks(benchmark_list, resource, load):
    benchmark_results = []
    for b in benchmark_list:
        benchmark = Benchmark(event_factory, b[2], b[0], b[1])
        benchmark.check_slo(resource, load)
        monitor = benchmark.monitor
        benchmark_results.append(monitor.cpu_utilization_timeseries)

    GraphVisualizer().view(
        "CPU Utilization",
        benchmark_results
    )

def run_single_experiment(benchmark: Benchmark, resource: int, load: int):
    benchmark.check_slo(resource, load)
    monitor = benchmark.monitor
    GraphVisualizer().view(
        "Resource Utilization",
        [monitor.cpu_utilization_timeseries,
         monitor.memory_utilization_timeseries,
         monitor.network_utilization_timeseries]
    )

def run_load_capacity_experiment(benchmark, resources, initial_guess, accuracy):
    benchmark.load_capacity(resources, initial_guess, accuracy)
    GraphVisualizer().view_load_capacity_results(benchmark.experiment_results)

def run_resource_demand_experiment(benchmark, load, initial_guess, accuracy):
    benchmark.resource_demand(load, initial_guess, accuracy)
    GraphVisualizer().view_load_capacity_results(benchmark.experiment_results)

def run_scalability_test_resource_demand(benchmarks):
    experiment_results = []
    for benchmark in benchmarks:
        experiment_results.append(benchmark.resource_demand_experiment([500, 1000, 1500, 2000]))

    plot_x = []
    plot_y = []
    for result in experiment_results:
        plot_x.append([x[0] for x in result])
        plot_y.append([x[1] for x in result])

    GraphVisualizer().show_plot(plot_x, plot_y, "", "Load", "Network Capacity")


def run_scalability_test_load_capacity(benchmarks):
    experiment_results = []
    for benchmark in benchmarks:
        experiment_results.append(benchmark.load_capacity_experiment([500, 1000, 1500, 2000]))

    plot_x=[]
    plot_y=[]
    for result in experiment_results:
        plot_x.append([x[0] for x in result])
        plot_y.append([x[1] for x in result])

    GraphVisualizer().show_plot(plot_x, plot_y, "", "Network Capacity", "Load")

def get_benchmarks():
    benchmark = Benchmark(
        event_factory,
        dfg_miner_intermediary,
        edge_topology,
        edge_miner
    )
    benchmark2 = Benchmark(
        event_factory,
        dfg_miner_intermediary,
        edge_topology,
        dfg_miner
    )
    benchmark3 = Benchmark(
        event_factory,
        dfg_miner_intermediary,
        fog_topology,
        dfg_miner
    )
    benchmark4 = Benchmark(
        event_factory,
        dfg_miner_central,
        cloud_topology,
        dfg_miner_cloud_sensor
    )
    return [
        benchmark,
        benchmark2,
        benchmark3,
        benchmark4
    ]

def run_load_capacity(benchmarks):
    run_scalability_test_load_capacity(benchmarks)

def run_resource_demand(benchmarks):
    run_scalability_test_resource_demand(benchmarks)

def run_test_for_metric():
    run_multiple_benchmarks([
        (edge_topology, edge_miner, dfg_miner_intermediary),
        (edge_topology, dfg_miner, dfg_miner_intermediary),
        (fog_topology, dfg_miner, dfg_miner_intermediary),
        (cloud_topology, dfg_miner_cloud_sensor, dfg_miner_central)
    ],
        200,
        50
    )

if __name__ == '__main__':
    event_factory: EventFactory = (
        EventFactory()
        .add_directory(directory="../../config/assemblyline")
        .add_file(filename="../../config/countbased.yaml"))

    edge_miner = lambda: EdgeDfgMiner()
    dfg_miner_intermediary = lambda: DfgMinerIntermediary()
    dfg_miner_central = lambda: DfgMinerCentral()
    dfg_miner_cloud_sensor = lambda: DfgMinerCloudSensor()
    dfg_miner = lambda: DfgMiner()

    edge_node = lambda name: ComputingNode(
        name,
        "sensor",
        cpu=CpuInstruction(lambda p: 2 * p, lambda p: p, 100),
        memory=StorageInstruction(lambda p: 2 * p, lambda p: p, 100),
        network=NetworkInstruction(lambda p: p, lambda p: p, 100)
    )

    edge_node_2 = lambda name: ComputingNode(
        name,
        "sensor",
        cpu=CpuInstruction(lambda p: 2 * p, lambda p: p, 100),
        memory=StorageInstruction(lambda p: 2 * p, lambda p: p, 100),
        network=NetworkInstruction(lambda p: 5*p, lambda p: p, 100)
    )

    fog_node = lambda name: ComputingNode(
        name,
        "intermediary",
        cpu=CpuInstruction(lambda p: 1.5 * p, lambda p: p, 150),
        memory=StorageInstruction(lambda p: 1.5 * p, lambda p: p, 150),
        network=NetworkInstruction(lambda p: 1.5 * p, lambda p: p, 150)
    )

    cloud_node = lambda name: ComputingNode(
        name,
        "cloud",
        cpu=CpuInstruction(lambda p: p, lambda p: p, 200),
        memory=StorageInstruction(lambda p: p, lambda p: p, 200),
        network=NetworkInstruction(lambda p: 1 * p, lambda p: p, 200)
    )

    edge_topology = (lambda: EdgeTopology(7).get_infrastructure(edge_node), "sensor-0", "sensor")
    fog_topology = (lambda: FogTopology(7, 3).get_infrastructure(edge_node, fog_node), "intermediary-0", "intermediary")
    cloud_topology = (lambda: CloudTopology(7).get_infrastructure(edge_node_2, cloud_node), "cloud", "cloud")

    run_test_for_metric()
    run_load_capacity(get_benchmarks())
    run_resource_demand(get_benchmarks())
