from network.fw.http_network_function import HttpNetworkFunction

class HttpNetwork:

    def __init__(self, network):
        self.network_functions = dict()
        self.network = network

    def add_network_function(self, name, func):
        self.network_functions[name] = HttpNetworkFunction(func, name)

    def get(self, name):
        return self.network_functions[name]

    def send_message(self, node_id, endpoint, payload):
        address = self.network.get_address(node_id)
        return self.network_functions[endpoint].call(address, endpoint, payload)

    def run(self, node):
        for network_function in self.network_functions:
            self.network_functions[network_function].run(node)
