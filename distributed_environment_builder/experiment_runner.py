from distributed_environment_builder.benchmark.benchmark import Benchmark
from distributed_environment_builder.graph_visualizer.graph_visualizer import GraphVisualizer


class ExperimentRunner:

    def run_single_experiment(self, benchmark: Benchmark, resource: int, load: int):
        benchmark.check_slo(resource, load)
        monitor = benchmark.monitor
        GraphVisualizer().view(
            "Resource Utilization",
            [
                monitor.cpu_utilization_timeseries,
                monitor.memory_utilization_timeseries,
                monitor.network_utilization_timeseries
            ]
        )

    def run_scalability_test_resource_demand(self, benchmarks):
        experiment_results = []
        for benchmark in benchmarks:
            experiment_results.append(benchmark.resource_demand_experiment([500, 1000, 1500, 2000], accuracy=20))

        plot_x = []
        plot_y = []
        for result in experiment_results:
            plot_x.append([x[0] for x in result])
            plot_y.append([x[1] for x in result])

        GraphVisualizer().show_plot(plot_x, plot_y, "", "Load", "Network Capacity")

    def run_scalability_test_load_capacity(self, benchmarks):
        experiment_results = []
        for benchmark in benchmarks:
            experiment_results.append(benchmark.load_capacity_experiment([500, 1000, 1500, 2000], accuracy=20))

        plot_x = []
        plot_y = []
        for result in experiment_results:
            plot_x.append([x[0] for x in result])
            plot_y.append([x[1] for x in result])

        GraphVisualizer().show_plot(plot_x, plot_y, "", "Network Capacity", "Load")