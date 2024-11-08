from abc import abstractmethod
from process_mining_core.datastructure.core.event import Event
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph


class EdgeNodeInterface:

    @abstractmethod
    def get_latest_event_with_case_id(self, case_id) -> Event | None:
        pass

    @abstractmethod
    def get_directly_follows_graph(self) -> DirectlyFollowsGraph:
        pass

