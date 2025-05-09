from process_mining_core.datastructure.core.counted_directly_follows_relation import CountedDirectlyFollowsRelation
from storage.case_activity_storage import CaseActivityStorage
from storage.storage import Storage

class DccStorage(Storage):

    def __init__(self, storage):
        self.directly_follows_storage: CountedDirectlyFollowsRelation = CountedDirectlyFollowsRelation(storage)
        self.case_activity_storage: CaseActivityStorage = CaseActivityStorage(storage)

    def store_last_event_of_case(self, case_activity_tuple):
        self.case_activity_storage.store_activity_for_case(case_activity_tuple)

    def get_activity_of_case(self, case_id):
        return self.case_activity_storage.get_activity_of_case(case_id)

    def get_directly_follows_graph(self):
        return self.directly_follows_storage

    def store_directly_follows_relation(self, directly_follows_relation):
        self.directly_follows_storage.insert(directly_follows_relation)

    def store_conformance_of_case(self, payload):
        super().store_conformance_of_case(payload)


