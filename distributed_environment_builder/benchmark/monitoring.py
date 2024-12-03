from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology


class TopologyMonitor:

    def __init__(self, topology: ComputingTopology):
        self.topology: ComputingTopology = topology
        self.processed_events = 0
        self.passed_time = 0

        self.average_processing_time = 0
        self.average_cpu_utilization = 0
        self.average_memory_utilization = 0
        self.average_network_utilization = 0

        self.processing_time_timeseries = []
        self.cpu_utilization_timeseries = []
        self.memory_utilization_timeseries = []
        self.network_utilization_timeseries = []

    def _get_all_hiis(self):
        return self.topology.get_cpus() | self.topology.get_memories() | self.topology.get_networks()

    def update(self, processed_events, time):
        self.processed_events = self.processed_events + processed_events
        self.passed_time = self.passed_time + time
        self.update_processing_time()
        self.update_cpu_utilization()
        self.update_memory_utilization()
        self.update_network_utilization()

    def reset(self):
        self.processed_events = 0
        self.passed_time = 0
        self.average_processing_time = 0
        self.average_cpu_utilization = 0
        self.average_memory_utilization = 0
        self.average_network_utilization = 0

    def update_processing_time(self):
        total_time = 0
        all_hiis = self._get_all_hiis()
        for hii in all_hiis:
            total_time = total_time + all_hiis[hii].get_time()
        self.average_processing_time = total_time / self.processed_events
        self.processing_time_timeseries.append(self.average_processing_time)

    def update_cpu_utilization(self):
        total_utilization = 0
        cpus = self.topology.get_cpus()
        for cpu in cpus:
            total_utilization += cpus[cpu].get_utilization(self.passed_time)
        self.average_cpu_utilization = total_utilization / len(cpus)
        self.cpu_utilization_timeseries.append(round(self.average_cpu_utilization, 3))

    def update_memory_utilization(self):
        total_utilization = 0
        memories = self.topology.get_memories()
        for memory in memories:
            total_utilization += memories[memory].get_utilization(self.passed_time)
        self.average_memory_utilization = total_utilization / len(memories)
        self.memory_utilization_timeseries.append(round(self.average_memory_utilization, 3))

    def update_network_utilization(self):
        total_utilization = 0
        networks = self.topology.get_networks()
        for network in networks:
            total_utilization += networks[network].get_utilization(self.passed_time)
        self.average_network_utilization = total_utilization / len(networks)
        self.network_utilization_timeseries.append(round(self.average_network_utilization, 3))


