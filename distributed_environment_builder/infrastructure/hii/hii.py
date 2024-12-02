from abc import ABC, abstractmethod


class Hii(ABC):

    @abstractmethod
    def get_time(self):
        pass

    @abstractmethod
    def get_utilization(self, time):
        pass