from distributed_environment_builder.benchmark.algo_sink import DfgMinerAlgoSink
from distributed_environment_builder.benchmark.distributed_algorithm import DistributedAlgorithm
from distributed_environment_builder.benchmark.monitoring import TopologyMonitor
from distributed_environment_builder.infrastructure.computing_node import ComputingNode
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology

class Benchmark:
    def __init__(
            self,
            event_factory,
            intermediary_algorithm,
            topology,
            source_algorithm
    ):
        self.monitor: TopologyMonitor = None
        self.distributed_algorithm = None
        self.computing_topology: ComputingTopology = None
        self.event_factory = event_factory
        self.intermediary_algorithm = intermediary_algorithm
        self.source_algorithm = source_algorithm
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
        topology: ComputingTopology = self.topology[0]()
        self.computing_topology = topology
        self.distributed_algorithm = DistributedAlgorithm(topology)
        self.monitor = TopologyMonitor(topology)

        for computing_node in topology.computing_nodes:
            node: ComputingNode = topology.computing_nodes[computing_node]

            algorithm = None
            if node.get_label() == "intermediary" or node.get_label() == "cloud":
                algorithm = self.intermediary_algorithm()
            elif node.get_label() == "sensor":
                algorithm = self.source_algorithm()

            self.distributed_algorithm.add_algorithm(
                node.get_name(),
                node.get_name(),
                algorithm
            )

        for i, node_id in enumerate(datasources):
            self.event_factory.add_sink(
                f"sensor-{i}",
                DfgMinerAlgoSink(
                    data_source_ref=[node_id],
                    miner=self.distributed_algorithm.get_algorithm(f"sensor-{i}")
                )
            )

    def hook(self, load):
        self.i = self.i +1
        if self.i % 10 == 0:
            print(self.distributed_algorithm.get_algorithm(self.topology[1]).get_directly_follows_graph_request()),
        self.monitor.update(1, float(1 / load)),
        print("CPU Utilization:", self.monitor.average_cpu_utilization),
        print("Memory Utilization:", self.monitor.average_memory_utilization),
        print("Network Utilization:", self.monitor.average_network_utilization),
        print("Processing Time:", self.monitor.average_processing_time)

    def check_slo(self, resource, load):
        self.init_algorithm()
        self.computing_topology.increase_network_capacities(resource, self.topology[2])
        self.computing_topology.increase_network_capacities(resource, "sensor")
        i = 0
        self.event_factory.run(
            hook=lambda: self.hook(load)
        )
        sli = self.monitor.average_network_utilization
        #sli=self.monitor.average_processing_time
        self.experiment_results.append((resource, load, sli))
        #return sli < 10.0
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

    def load_capacity_experiment(self, test_values):
        result = []
        for test_value in test_values:
            result.append((test_value, self.load_capacity(test_value, 100, 10)))
        return result

    def resource_demand_experiment(self, test_values):
        result = []
        for test_value in test_values:
            result.append((test_value, self.resource_demand(test_value, 100, 10)))
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