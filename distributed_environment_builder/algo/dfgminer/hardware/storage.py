from typing import Dict

from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event

class StorageDfgMiner:

    def __init__(self, storage):
        self.storage = storage
        self.directly_follows_relations: Dict[DirectlyFollowsRelation, int] = dict()
        self.events: Dict[str, Event] = dict()

    def store_directly_follows_relation(self, directly_follows_relation: DirectlyFollowsRelation):
        if directly_follows_relation in self.directly_follows_relations:
            new_count = self.directly_follows_relations[directly_follows_relation] + 1
        else:
            self.storage.store(payload=2)
            new_count = 1
        self.directly_follows_relations[directly_follows_relation] = new_count

    def store_event(self, event):
        self.events[event.caseid] = event
        self.storage.store(payload=1)

    def get_latest_event_with_case_id(self, case_id) -> Event | None:
        self.storage.store(payload=1)
        if case_id in self.events:
            return self.events[case_id]
        return None

    def get_all_directly_follows_relations(self) -> Dict[DirectlyFollowsRelation, int]:
        self.storage.store(payload=1)
        return self.directly_follows_relations