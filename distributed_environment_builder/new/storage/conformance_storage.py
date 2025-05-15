from conformance_score import ConformanceScore
from storage.conformance_value import ConformanceValues

class ConformanceStorage:
    def __init__(self, storage):
        self.storage = storage

    def store_conformance_values(self, conformance_values: ConformanceValues):
        self.storage[conformance_values.case_id] = conformance_values

    def retrieve_conformance_values(self, case_id):
        if case_id in self.storage:
            return self.storage[case_id]
        return ConformanceValues(case_id, None, ConformanceScore())

    def update_last_event_of_case(self, case_id, activity):
        conformance_values: ConformanceValues = self.retrieve_conformance_values(case_id)
        if conformance_values:
            self.store_conformance_values(ConformanceValues(case_id, activity, conformance_values.conformance))
        else:
            self.store_conformance_values(ConformanceValues(case_id, activity, ConformanceScore()))


    def update_conformance(self, case_id, conformance):
        conformance_values: ConformanceValues = self.retrieve_conformance_values(case_id)
        if conformance_values:
            self.store_conformance_values(ConformanceValues(case_id, conformance_values.last_activity, conformance))
        else:
            self.store_conformance_values(ConformanceValues(case_id, None, conformance))
