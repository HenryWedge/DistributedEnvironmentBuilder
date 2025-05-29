from abc import ABC, abstractmethod


class RequestGenerator(ABC):

    @abstractmethod
    def get_request(self):
        pass