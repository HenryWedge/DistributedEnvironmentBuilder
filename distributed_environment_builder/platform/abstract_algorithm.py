from abc import ABC, abstractmethod

class AbstractAlgorithm(ABC):

    @abstractmethod
    def assign_to_node(
            self,
            node_id,
            computing_topology):
        pass
