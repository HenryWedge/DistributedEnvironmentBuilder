from abc import abstractmethod, ABC
from typing import List, Dict

from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event


class StorageEdgeInterface(ABC):

    @abstractmethod
    def store_directly_follows_relation(self, directly_follows_relation: DirectlyFollowsRelation):
        pass

    @abstractmethod
    def store_event(self, event):
        pass

    @abstractmethod
    def get_latest_event_with_case_id(self, case_id) -> Event:
        pass

    @abstractmethod
    def get_all_directly_follows_relations(self) -> Dict[DirectlyFollowsRelation, int]:
        pass
