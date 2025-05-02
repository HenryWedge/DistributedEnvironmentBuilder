from abc import ABC


class NetworkFunction(ABC):

    def call(self, payload):
        pass

    def run(self):
        pass