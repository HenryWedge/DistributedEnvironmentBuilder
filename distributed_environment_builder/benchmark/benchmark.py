from distributed_environment_builder.algo.dfgminer.dfg_miner import DfgMiner
from distributed_environment_builder.algo.dfgminer.dfg_miner_intermediary import DfgMinerIntermediary
from distributed_environment_builder.algo.edgemine.edge_miner import EdgeDfgMiner
from distributed_environment_builder.benchmark.algo_sink import DfgMinerAlgoSink
from distributed_environment_builder.benchmark.distributed_algorithm import DistributedAlgorithm
from distributed_environment_builder.benchmark.monitoring import TopologyMonitor
from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology
from distributed_environment_builder.topology.edge_topology import EdgeTopology
from distributed_environment_builder.topology.fog_topology import FogTopology


class Benchmark:
    def __init__(self, event_factory, is_improved, is_sourced):
        self.event_factory = event_factory
        self.computing_topology: ComputingTopology = None
        self.is_improved = is_improved
        self.is_sourced = is_sourced
        self.init_algorithm(event_factory)

    def init_algorithm(self, event_factory):
        datasources = [
            "GoodsDelivery",
            "MaterialPreparation",
            "AssemblyLineSetup",
            "Assembling",
            "QualityControl",
            "Packaging",
            "Shipping",
        ]

        if self.is_sourced:
            self.computing_topology = EdgeTopology(len(datasources)).get_infrastructure()
        else:
            self.computing_topology = FogTopology(len(datasources), 3).get_infrastructure()

        self.distributed_algorithm = DistributedAlgorithm(self.computing_topology)
        self.monitor = TopologyMonitor(self.computing_topology)

        for i, computing_node in enumerate(self.computing_topology.get_nodes_with_label("intermediary")):
            self.distributed_algorithm.add_algorithm(f"intermediary-{i}", computing_node.get_name(), DfgMinerIntermediary())

        for i, node_id in enumerate(datasources):
            generic_node_id = f"sensor-{i}"
            if self.is_improved:
                algorithm = EdgeDfgMiner()
            else:
                algorithm = DfgMiner()

            self.distributed_algorithm.add_algorithm(generic_node_id, generic_node_id, algorithm)
            event_factory.add_sink(generic_node_id, DfgMinerAlgoSink(data_source_ref=[node_id], miner=algorithm))

    def check_slo(self, value):
        self.init_algorithm(self.event_factory)
        self.event_factory.run(
            hook=lambda: (
                self.distributed_algorithm.get_algorithm("sensor-0").get_directly_follows_graph_request(),
                self.monitor.update(1, float(1/value)),
                print("CPU Utilization:", self.monitor.cpu_utilization()),
                print("Memory Utilization:", self.monitor.memory_utilization()),
                print("Network Utilization:", self.monitor.network_utilization()),
                #print("Processing Time:", self.monitor.average_processing_time())
            )
        )
        return self.monitor.network_utilization() < 1.0


    def check_slo_capacity(self, value):
        self.init_algorithm(self.event_factory)
        self.computing_topology.increase_network_capacities(value)
        self.event_factory.run(
            hook=lambda: (
                self.distributed_algorithm.get_algorithm("sensor-0").get_directly_follows_graph_request(),
                self.monitor.update(1, float(1/100)),
                #print("Network Utilization:", self.monitor.network_utilization()),
                #print("Processing Time:", self.monitor.average_processing_time())
            )
        )
        return self.monitor.network_utilization() < 1.0

    def run(self, initial_guess, accuracy):
        success = 0
        fail = 0
        guess = initial_guess
        while not success or not fail or fail - success > accuracy:
            print("Try for value: ", guess)
            if self.check_slo_capacity(guess):
                success = guess
                if fail:
                    guess = (success + fail) / 2
                else:
                    guess = guess * 2
            else:
                fail = guess
                if success:
                    guess = (success + fail) / 2
                else:
                    guess = guess / 2
        print(guess)
        return guess

    def run2(self, initial_guess, accuracy):
        success = 0
        fail = 0
        guess = initial_guess
        while not success or not fail or abs(success - fail) > accuracy:
            print("Try for value: ", guess)
            if self.check_slo_capacity(guess):
                success = guess
                if fail:
                    guess = (success + fail) / 2
                else:
                    guess = guess / 2
            else:
                fail = guess
                if success:
                    guess = (success + fail) / 2
                else:
                    guess = guess * 2
        print(guess)
        return guess
