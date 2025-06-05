from network.fw.network import Network

class MockNetwork(Network):

    def __init__(self, network_router, initial_time, initial_resource, throughput, payload):
        self.network_functions = dict()
        self.network = network_router
        self.initial_time = initial_time
        self.initial_resource = initial_resource
        self.throughput = throughput
        self.consumed_time = 0
        self.consumed_resource = 0
        self.payload = payload

    def add_network_function(self, name, func, clazz):
        self.network_functions[name] = func

    def get(self, name):
        return self.network_functions[name]

    def get_address(self):
        return self

    def has_node(self, node_id):
        return self.network.has_node(node_id)

    def broadcast(self, endpoint, payload):
        results = dict()
        nodes = self.network.get_all_addresses()
        for node in nodes:
            result = self.send_message(node, endpoint, payload)
            if result:
                results[node] = result
        return results

    def time_utilization(self, event_delta):
        utilization = self.consumed_time / event_delta
        self.consumed_time = 0
        return utilization

    def resource_utilization(self, velocity):
        utilization = (self.consumed_resource * velocity) / self.throughput
        self.consumed_resource = 0
        return utilization

    def send_message(self, node_id, endpoint, payload):
        self.consumed_time = self.consumed_time + self.initial_time + (self.payload / self.throughput)
        self.consumed_resource = self.consumed_resource + self.initial_resource + self.payload

        node_network = self.network.get_address(node_id)
        return node_network.network_functions[endpoint](payload)

    def run(self, node):
        pass
