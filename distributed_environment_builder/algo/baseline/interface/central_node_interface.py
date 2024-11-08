from abc import abstractmethod, ABC

from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph

class CentralNodeInterface(ABC):

    @abstractmethod
    def get_directly_follows_graph(self) -> DirectlyFollowsGraph:
        pass