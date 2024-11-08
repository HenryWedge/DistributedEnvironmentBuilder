from abc import ABC, abstractmethod


class Network(ABC):

    @abstractmethod
    def get_used_bandwidth(self):
        pass