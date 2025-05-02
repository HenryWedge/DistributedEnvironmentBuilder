class HelloTopology:

    def __init__(self):
        self.networks = dict()
        self.nodes = dict()

    def add_network(self, network_id, network):
        self.networks[network_id] = network

    def add_node(self, node_id, node):
        self.nodes[node_id] = node

    def get_node(self, node_id):
        return self.nodes[node_id]

    def deploy_algorithm(self, node_id, algorithm):
        algorithm.assign_to_node(self.nodes[node_id])

    def run(self, algorithm, node):
        algorithm.run_on_node(self.nodes[node])