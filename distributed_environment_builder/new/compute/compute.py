from abc import ABC, abstractmethod


class Compute(ABC):

    @abstractmethod
    def time_utilization(self, event_delta):
        pass

    @abstractmethod
    def resource_utilization(self, time_delta):
        pass

    @abstractmethod
    def run(self, f, p):
        pass