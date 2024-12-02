from typing import List

from process_mining_core.datastructure.core.event import Event

class CpuDfgMiner:
    def __init__(self, cpu):
        self.cpu = cpu

    def compute_largest_timestamp(self, events: List[Event]) -> Event:
        event_with_largest_timestamp = events[0]
        for event in events:
            if event is None:
                continue
            self.cpu.compute(payload=1)
            if event.timestamp > event_with_largest_timestamp.timestamp:
                event_with_largest_timestamp = event
        return event_with_largest_timestamp