class MockNetwork:

    def __init__(self):
        self.network_functions = dict()

    def add_network_function(self, name, func):
        self.network_functions[name] = func

    def get(self, name):
        return self.network_functions[name]

    def send_message(self, node_id, endpoint, payload):
        return self.network_functions[endpoint](payload=payload)

    def run(self, node):
        pass
