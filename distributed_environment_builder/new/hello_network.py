class HelloNetwork:

    def __init__(self):
        self.addresses = dict()

    def add_network_address(self, node_id, address):
        self.addresses[node_id] = address

    def get_address(self, node_id):
        return self.addresses[node_id]

    def get_all_addresses(self):
        return self.addresses
