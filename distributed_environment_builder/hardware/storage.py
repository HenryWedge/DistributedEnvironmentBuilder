from abc import ABC, abstractmethod

class Storage(ABC):

    @abstractmethod
    def get_size_stored_objects(self):
        pass