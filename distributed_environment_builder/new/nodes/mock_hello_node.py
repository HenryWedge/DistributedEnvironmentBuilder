from nodes.node_interface import NodeInterface


class MockHelloNode(NodeInterface):

    def __init__(self, node_id, network, storage):
        self.endpoints = dict()
        self.node_id = node_id
        self.network = network
        self.storage = storage

    def run(self):
        pass