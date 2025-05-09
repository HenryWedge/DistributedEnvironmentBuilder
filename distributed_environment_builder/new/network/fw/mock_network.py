import time


class MockNetwork:

    def __init__(self, network, delay):
        self.network_functions = dict()
        self.delay = delay
        self.network = network

    def add_network_function(self, name, func, clazz):
        self.network_functions[name] = func

    def get(self, name):
        return self.network_functions[name]

    def get_address(self):
        return self

    def send_message(self, node_id, endpoint, payload):
        time.sleep(self.delay)
        node_network = self.network.get_address(node_id)
        return node_network.network_functions[endpoint](payload)

    def run(self, node):
        pass
