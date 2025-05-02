class HelloNetwork:

    def __init__(self):
        self.network_accesses = dict()
        self.addresses = dict()

    def add_network_access(self, node_id, address, network_access):
        self.network_accesses[node_id] = network_access
        self.addresses[node_id] = address

    def get_address(self, node_id):
        return self.addresses[node_id]

    def send_message(self, node_id, endpoint, payload):
        return self.network_accesses[node_id].send_message(self.addresses[node_id], endpoint, payload)