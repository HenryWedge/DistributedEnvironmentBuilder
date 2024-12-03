from distributed_environment_builder.infrastructure.computing_topology import ComputingTopology


class TopologyMonitor:

    def __init__(self, topology: ComputingTopology):
        self.topology: ComputingTopology = topology
        self.processed_events = 0
        self.passed_time = 0
        self.cpu_utilization_timeseries = []
        self.memory_utilization_timeseries = []
        self.network_utilization_timeseries = []

    def _get_all_hiis(self):
        return self.topology.get_cpus() | self.topology.get_memories() | self.topology.get_networks()

    def update(self, processed_events, time):
        self.processed_events = self.processed_events + processed_events
        self.passed_time = self.passed_time + time


    def reset(self):
        self.processed_events = 0
        self.passed_time = 0

    def average_processing_time(self):
        total_time = 0
        all_hiis = self._get_all_hiis()
        for hii in all_hiis:
            total_time = total_time + all_hiis[hii].get_time()
        return total_time / self.processed_events

    def average_utilization(self):
        total_utilization = 0
        all_hiis = self._get_all_hiis()
        for hiis in all_hiis:
            total_utilization = total_utilization + all_hiis[hiis].get_utilization(self.passed_time)
        return total_utilization / len(self._get_all_hiis())

    def cpu_utilization(self):
        total_utilization = 0
        cpus = self.topology.get_cpus()
        for cpu in cpus:
            total_utilization += cpus[cpu].get_utilization(self.passed_time)
        avg_utilization = total_utilization / len(cpus)
        self.cpu_utilization_timeseries.append(round(avg_utilization, 3))
        return avg_utilization

    def network_utilization(self):
        total_utilization = 0
        networks = self.topology.get_networks()
        for network in networks:
            total_utilization += networks[network].get_utilization(self.passed_time)
        avg_utilization = total_utilization / len(networks)
        self.network_utilization_timeseries.append(round(avg_utilization, 3))
        return avg_utilization

    def memory_utilization(self):
        total_utilization = 0
        memories = self.topology.get_memories()
        for memory in memories:
            total_utilization += memories[memory].get_utilization(self.passed_time)
        avg_utilization = total_utilization / len(memories)
        self.memory_utilization_timeseries.append(round(avg_utilization, 3))
        return avg_utilization
