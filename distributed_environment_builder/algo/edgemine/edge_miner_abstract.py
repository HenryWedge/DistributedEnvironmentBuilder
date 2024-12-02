from abc import ABC, abstractmethod


class AbstractEdgeMiner(ABC):

    @abstractmethod
    def get_latest_activity_with_case_id(self, case_id):
        pass

    @abstractmethod
    def inform_predecessor(self, case_id, node_id, activity):
        pass
