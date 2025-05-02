class HelloNetwork:

    def __init__(self):
        self.nodes = dict()

    def add_node(self, node):
        self.nodes[node.node_id] = node

    def get_node(self, node_id):
        return self.nodes[node_id]

    def send_message(self, node_id, endpoint, payload):
        return self.get_node(node_id).call_endpoint(endpoint, payload)