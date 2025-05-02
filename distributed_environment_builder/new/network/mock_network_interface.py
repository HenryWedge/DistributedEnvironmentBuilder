from network_interface import HelloNetworkInterface

class MockNetworkInterface(HelloNetworkInterface):

    def __init__(self, node_id, algorithm):
        self.node_id = node_id
        self.algorithm = algorithm

    def get_hello(self, payload=dict()):
        print(self.algorithm.get_hello(payload))

    def get_hi(self, payload=dict()):
        print(self.algorithm.get_hi(payload))