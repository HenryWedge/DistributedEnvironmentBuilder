from abc import ABC

class DccStorageInterface(ABC):

    def store_last_event_of_case(self, payload):
        pass

    def get_directly_follows_graph(self):
        pass

    def store_directly_follows_relation(self, payload):
        pass

    def store_conformance_of_case(self, payload):
        pass