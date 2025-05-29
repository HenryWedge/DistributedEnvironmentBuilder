from abc import abstractmethod, ABC


class Infrastructure(ABC):

    @abstractmethod
    def receive_event(self, location, event):
        pass