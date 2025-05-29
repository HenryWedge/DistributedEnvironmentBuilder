from abc import ABC, abstractmethod


class Monitor(ABC):

    @abstractmethod
    def monitor(self):
        pass