from abc import ABC, abstractmethod

from process_mining_core.datastructure.core.event import Event


class LoadGenerator(ABC):

    @abstractmethod
    def next_event(self) -> Event:
        pass