class HelloNode:

    def __init__(self, node_id, network, storage, category, datasource):
        self.node_id = node_id
        self.network = network
        self.storage = storage
        self.category = category
        self.datasource = datasource
        self.storages = dict()

    def get_storage(self, name):
        new_storage = self.storage(f"{self.node_id}-{name}")
        self.storages[name] = new_storage
        return new_storage

    def get_storage_utilization(self):
        utilization = 0
        for storage in self.storages:
            utilization = utilization + self.storages[storage].get_utilization()
        return utilization

    def run(self):
        self.network.run(self)
