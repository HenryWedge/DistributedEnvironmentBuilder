from abc import ABC, abstractmethod
from typing import List

class Algorithm(ABC):

    def __init__(self, protocol_ids):
        self.protocol_ids = protocol_ids

    @abstractmethod
    def assign_to_node(
            self,
            node_id: str,
            computing_topology):
        pass

    def get_protocol_ids(self) -> List[str]:
        return self.protocol_ids
