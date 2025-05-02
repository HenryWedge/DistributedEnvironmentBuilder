class SayHelloAlgorithm:
    def __init__(self):
        self.node_id = None

    def run_on_node(self, node):
        self.node_id = node.node_id
        self.storage = node.storage
        self.network_access = node.network_access
        node.network_access.add_network_function("hi", self.get_hi)
        node.network_access.add_network_function("hello", self.get_hello)
        node.network_access.add_network_function("event", self.process_event)

    def get_hello(self, payload):
        print(f"Hello, {payload.get("message")}!")
        self.network_access.send_message(node_id="node1", endpoint="hi", payload=dict())
        return "hello"

    def get_hi(self, payload):
        print(f"Hi from node {self.node_id}!")
        return "hi"

    def process_event(self, payload):
        self.storage.store_item(payload)
        self.network_access.send_message(node_id="node2", endpoint="hi", payload=dict())
        print(payload)
        return payload

    def get_model(self):
        self.storage.get_storage()

