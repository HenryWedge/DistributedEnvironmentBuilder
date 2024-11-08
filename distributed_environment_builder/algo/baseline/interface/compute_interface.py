from abc import abstractmethod
from typing import List

from process_mining_core.datastructure.core.event import Event


class ComputeEdgeInterface:

    @abstractmethod
    def compute_largest_timestamp(self, events: List[Event]) -> Event:
        pass