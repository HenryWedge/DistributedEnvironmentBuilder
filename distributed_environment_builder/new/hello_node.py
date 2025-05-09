class HelloNode:

    def __init__(self, node_id, network, storage, category, datasource):
        self.node_id = node_id
        self.network = network
        self.storage = storage
        self.category = category
        self.datasource = datasource

    def run(self):
        self.network.run(self)
