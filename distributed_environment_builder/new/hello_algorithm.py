class SayHelloAlgorithm:
    def __init__(self):
        self.node_id = None
        self.network = None

    def run_on_node(self, node):
        self.node_id = node.node_id
        self.network = node.network
        self.storage = node.storage
        node.register_endpoint("hello", self.get_hello)
        node.register_endpoint("hi", self.get_hi)
        node.register_endpoint("event", self.process_event)
        node.run()

    def get_hello(self, payload):
        print(f"Hello, {payload.get("message")}!")
        self.network.send_message(node_id=8082, endpoint="hi", payload=dict())
        return "hello"

    def get_hi(self, payload):
        print("Hi!")
        return "hi"

    def process_event(self, payload):
        self.storage.store_item(payload)
        self.network.send_message(node_id=8084, endpoint="hi", payload=dict())
        print(payload)
        return payload

    def get_model(self):
        self.storage.get_storage()

