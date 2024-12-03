from distributed_environment_builder.benchmark.benchmark import Benchmark
from distributed_environment_builder.graph_visualizer.graph_visualizer import GraphVisualizer
from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':

    event_factory: EventFactory = (
        EventFactory()
        .add_directory(directory="../../../DistributedEventFactory/config/datasource/assemblyline")
        .add_file(filename="../../../DistributedEventFactory/config/simulation/countbased.yaml"))

    benchmark = Benchmark(event_factory, is_sourced=False, is_improved=False)
    benchmark.check_slo(15)#run2(1200, 1)
    GraphVisualizer().view(
        benchmark.monitor.cpu_utilization_timeseries,
        benchmark.monitor.memory_utilization_timeseries,
        benchmark.monitor.network_utilization_timeseries,
    )
