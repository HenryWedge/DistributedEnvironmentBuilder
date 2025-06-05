import requests

from network_interface import HelloNetworkInterface


class HttpNetworkInterface(HelloNetworkInterface):

    def __init__(self, node_id):
        self.node_id = node_id

    def get_hello(self, payload=dict()):
        print(requests.get(url=f"http://localhost:{self.node_id}/hello").content)

    def get_hi(self, payload=dict()):
        print(requests.get(url=f"http://localhost:{self.node_id}/hi").content)