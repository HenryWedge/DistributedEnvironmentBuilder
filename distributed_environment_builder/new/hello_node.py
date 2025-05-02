class HelloNode:

    def __init__(self, node_id, network, storage):
        self.node_id = node_id
        self.network = network
        self.storage = storage

    def run(self):
        self.network.run(self)
