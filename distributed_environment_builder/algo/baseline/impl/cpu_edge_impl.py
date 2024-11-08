from typing import List

from distributed_environment_builder.algo.baseline.interface.compute_interface import \
    ComputeEdgeInterface
from DistributedEnvironmentBuilder.distributed_environment_builder.hardware.cpu import Cpu
from process_mining_core.datastructure.core.event import Event

class CpuEdgeNode(ComputeEdgeInterface, Cpu):

    def __init__(self, instruction_cost):
        self.instruction_cost = instruction_cost
        self.total_cost = 0

    def get_time(self):
        return self.total_cost

    def compute_largest_timestamp(self, events: List[Event]) -> Event:
        event_with_largest_timestamp = events[0]

        for event in events:
            if event is None:
                continue
            self.total_cost += self.instruction_cost
            if event.timestamp > event_with_largest_timestamp.timestamp:
                event_with_largest_timestamp = event

        return event_with_largest_timestamp