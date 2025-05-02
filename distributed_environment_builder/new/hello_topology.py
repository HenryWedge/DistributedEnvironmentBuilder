from hello_network import HelloNetwork


class HelloTopology:

    def __init__(self):
        self.networks = dict()
        self.nodes = dict()
        self.network_address_resolution = HelloNetwork()

    def add_network(self, network_id, network):
        self.networks[network_id] = network

    def add_node(self, node_id, node):
        self.nodes[node_id] = node
        self.network_address_resolution.add_network_address(node_id, node.network.get_address())

    def get_node(self, node_id):
        return self.nodes[node_id]

    def deploy_algorithm(self, node_id, algorithm):
        algorithm.assign_to_node(self.nodes[node_id])

    def deploy(self, algorithm, node_id):
        algorithm.run_on_node(self.nodes[node_id])

    def run(self, node_id):
        self.nodes[node_id].run()
