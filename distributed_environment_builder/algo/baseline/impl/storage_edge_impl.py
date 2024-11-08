from typing import Dict

from distributed_environment_builder.algo.baseline.interface.store_interface import StorageEdgeInterface
from distributed_environment_builder.hardware.storage import Storage
from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event

class StorageEdgeNode(StorageEdgeInterface, Storage):

    def __init__(self, storage_cost):
        self.storage_cost: int = storage_cost
        self.directly_follows_relations: Dict[DirectlyFollowsRelation, int] = dict()
        self.events: Dict[str, Event] = dict()

    def get_size_stored_objects(self):
        return self.storage_cost * (len(self.directly_follows_relations) + len(self.events))

    def store_directly_follows_relation(self, directly_follows_relation: DirectlyFollowsRelation):
        new_count = 1
        if directly_follows_relation in self.directly_follows_relations:
            new_count = self.directly_follows_relations[directly_follows_relation] + 1

        self.directly_follows_relations[directly_follows_relation] = new_count


    def store_event(self, event):
        self.events[event.caseid] = event

    def get_latest_event_with_case_id(self, case_id) -> Event | None:
        if case_id in self.events:
            return self.events[case_id]
        return None

    def get_all_directly_follows_relations(self) -> Dict[DirectlyFollowsRelation, int]:
        return self.directly_follows_relations

