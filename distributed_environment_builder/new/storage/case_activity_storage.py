from storage.case_actity_tuple import CaseActivityTuple

class CaseActivityStorage:

    def __init__(self, storage=dict()):
        self.storage = storage

    def get_activity_of_case(self, case_id):
        if case_id in self.storage:
            return self.storage[case_id]
        return None

    def store_activity_for_case(self, case_activity_tuple: CaseActivityTuple):
        self.storage[case_activity_tuple.case] = case_activity_tuple.activity
