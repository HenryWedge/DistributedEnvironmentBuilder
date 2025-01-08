from distributed_environment_builder.benchmark.algo_sink import DfgMinerAlgoSink
from distributed_environment_builder.benchmark.deployed_algorithm import DeployedAlgorithm
from distributed_environment_builder.benchmark.monitoring import TopologyMonitor
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology
from distributed_event_factory.event_factory import EventFactory


class Benchmark:
    def __init__(
            self,
            event_factory,
            topology,
            distributed_algorithm,
            request_node_id
    ):
        self.monitor: TopologyMonitor = None
        self.deployed_algorithm = None
        self.computing_topology: ComputingTopology = None
        self.event_factory: EventFactory = event_factory
        self.distributed_algorithm = distributed_algorithm
        self.request_node_id = request_node_id
        self.topology = topology
        self.experiment_results = []
        self.init_algorithm()
        self.i = 0

    def init_algorithm(self):
        datasources = [
            "GoodsDelivery",
            "MaterialPreparation",
            "AssemblyLineSetup",
            "Assembling",
            "QualityControl",
            "Packaging",
            "Shipping",
        ]

        self.i = 0
        topology: ComputingTopology = self.topology()
        self.computing_topology = topology
        self.monitor = TopologyMonitor(topology)
        self.deployed_algorithm = DeployedAlgorithm(topology, self.distributed_algorithm).deploy()

        for i, node_id in enumerate(datasources):
            self.event_factory.add_sink(
                f"sensor-{i}",
                DfgMinerAlgoSink(
                    data_source_ref=[node_id],
                    miner=self.deployed_algorithm.get_algorithm(f"sensor-{i}")
                )
            )

    def hook(self, load):
        self.i = self.i + 1
        if self.i % 10 == 0:
            print(self.deployed_algorithm.get_algorithm(self.request_node_id).get_directly_follows_graph_request()),
        self.monitor.update(1, float(1 / load)),
        print("CPU Utilization:", self.monitor.average_cpu_utilization),
        print("Memory Utilization:", self.monitor.average_memory_utilization),
        print("Network Utilization:", self.monitor.average_network_utilization),
        print("Processing Time:", self.monitor.average_processing_time)

    def check_slo(self, resource, load):
        self.init_algorithm()
        self.computing_topology.increase_network_capacities(resource, "sensor")
        self.event_factory.run(
            hook=lambda: self.hook(load)
        )
        sli = self.monitor.average_network_utilization
        self.experiment_results.append((resource, load, sli))
        return sli < 0.95

    def _next_guess(self, last_guess, bound_value, is_increase):
        if bound_value:
            return (last_guess + bound_value) / 2
        else:
            if is_increase:
                last_guess = last_guess * 2
            else:
                last_guess = last_guess / 2
            return last_guess

    def resource_demand(self, load, initial_guess, accuracy):
        return self.run(
            initial_guess,
            accuracy,
            slo=lambda guess: self.check_slo(guess, load),
            is_increase=False
        )

    def load_capacity(self, resource, initial_guess, accuracy):
        return self.run(
            initial_guess,
            accuracy,
            slo=lambda guess: self.check_slo(resource, guess),
            is_increase=True
        )

    def load_capacity_experiment(self, test_values, accuracy):
        result = []
        for test_value in test_values:
            result.append((test_value, self.load_capacity(test_value, 100, accuracy)))
        return result

    def resource_demand_experiment(self, test_values, accuracy):
        result = []
        for test_value in test_values:
            result.append((test_value, self.resource_demand(test_value, 100, accuracy)))
        return result

    def run(self, initial_guess, accuracy, slo, is_increase):
        success = 0
        fail = 0
        guess = initial_guess
        while not success or not fail or abs(success - fail) > accuracy:
            if slo(guess):
                success = guess
                guess = self._next_guess(success, fail, is_increase)
            else:
                fail = guess
                guess = self._next_guess(fail, success, not is_increase)
        print(guess)
        return guess
