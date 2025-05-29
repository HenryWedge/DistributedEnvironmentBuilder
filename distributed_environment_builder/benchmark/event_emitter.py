from abc import ABC, abstractmethod

from process_mining_core.datastructure.core.event import Event

class EventEmitter(ABC):

    @abstractmethod
    def get_event(self) -> Event:
        pass