from abc import ABC


class NetworkFunction(ABC):

    def call(self, address, endpoint, payload):
        pass

    def run(self, node):
        pass