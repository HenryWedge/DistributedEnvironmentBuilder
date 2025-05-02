class MockNetwork:

    def __init__(self, network):
        self.network_functions = dict()
        self.network = network

    def add_network_function(self, name, func):
        self.network_functions[name] = func

    def get(self, name):
        return self.network_functions[name]

    def send_message(self, node_id, endpoint, payload):
        node = self.network.get_address(node_id)
        return node.network.network_functions[endpoint](payload=payload)

    def run(self, node):
        pass
