from abc import ABC

class NodeInterface(ABC):

    def call_endpoint(self, endpoint, payload=dict()):
        pass

    def register_endpoint(self, endpoint, func, methods=["GET"]):
        pass

    def run(self):
        pass