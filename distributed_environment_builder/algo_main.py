from distributed_environment_builder.algo.dfgminer.dfg_miner import DfgMiner
from distributed_environment_builder.algo.dfgminer.dfg_miner_intermediary import DfgMinerIntermediary
from distributed_environment_builder.algo.edgemine.edge_miner import EdgeDfgMiner
from distributed_environment_builder.benchmark.benchmark import Benchmark
from distributed_environment_builder.graph_visualizer.graph_visualizer import GraphVisualizer
from distributed_environment_builder.topology.edge_topology import EdgeTopology
from distributed_environment_builder.topology.fog_topology import FogTopology
from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':
    event_factory: EventFactory = (
        EventFactory()
        .add_directory(directory="../../../DistributedEventFactory/config/datasource/assemblyline")
        .add_file(filename="../../../DistributedEventFactory/config/simulation/countbased.yaml"))

    edge_miner= lambda: EdgeDfgMiner()
    dfg_miner_intermediary = lambda: DfgMinerIntermediary()
    dfg_miner = lambda: DfgMiner()

    edge_topology = lambda: EdgeTopology(7).get_infrastructure()
    fog_topology = lambda: FogTopology(7, 3).get_infrastructure()
    benchmark = Benchmark(event_factory, dfg_miner_intermediary, edge_topology, dfg_miner)

    benchmark.check_slo(200, 60)
    monitor = benchmark.monitor
    GraphVisualizer().view(
        monitor.cpu_utilization_timeseries,
        monitor.memory_utilization_timeseries,
        monitor.network_utilization_timeseries
    )
    #benchmark.load_capacity(200, 100, 1)
    #print(benchmark.resource_demand_experiment([500, 1000, 1500, 2000]))
    #GraphVisualizer().view_load_capacity_results(benchmark.experiment_results)

