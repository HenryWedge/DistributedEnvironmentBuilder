from node_interface import NodeInterface

class MockHelloNode(NodeInterface):

    def __init__(self, node_id, network, storage):
        self.endpoints = dict()
        self.node_id = node_id
        self.network = network
        self.storage = storage
        network.add_node(self)

    def call_endpoint(self, endpoint, payload=dict()):
        return self.endpoints[endpoint](payload)

    def register_endpoint(self, endpoint, func, methods=["GET"]):
        self.endpoints[endpoint] = lambda payload: func(payload)

    def run(self):
        pass