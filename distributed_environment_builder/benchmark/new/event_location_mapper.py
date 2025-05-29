from abc import abstractmethod, ABC

from process_mining_core.datastructure.core.event import Event

class EventLocationMapper(ABC):

    @abstractmethod
    def get_location(self, event: Event) -> str:
        pass