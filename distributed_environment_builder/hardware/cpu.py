from abc import ABC, abstractmethod


class Cpu(ABC):

    @abstractmethod
    def get_time(self) -> int:
        pass
