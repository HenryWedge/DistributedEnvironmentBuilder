class HelloNetwork:

    def __init__(self):
        self.network_accesses = dict()
        self.addresses = dict()

    def add_network_address(self, node_id, address):
        self.addresses[node_id] = address

    def get_address(self, node_id):
        return self.addresses[node_id]
