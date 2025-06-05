from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def time_utilization(self, event_delta):
        pass

    @abstractmethod
    def resource_utilization(self, time_delta):
        pass
