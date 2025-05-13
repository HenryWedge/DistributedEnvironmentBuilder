from threading import Thread
import uuid

from flask import Flask
from network.fw.http_network_function import HttpNetworkFunction
from network.fw.network import Network

class HttpNetwork(Network):
    def __init__(self, network, port):
        self.network_functions = dict()
        self.app = Flask(uuid.uuid4().hex.upper())
        self.network = network
        self.port = port

    def add_network_function(self, name, func, clazz):
        self.network_functions[name] = HttpNetworkFunction(self.app, func, name, clazz)

    def get(self, name):
        return self.network_functions[name]

    def get_address(self):
        return f"localhost:{self.port}"

    def send_message(self, node_id, endpoint, payload):
        address = self.network.get_address(node_id)
        return self.network_functions[endpoint].call(address, endpoint, payload)

    def broadcast(self, endpoint, payload):
        results = dict()
        nodes = self.network.get_all_addresses()
        for node in nodes:
            result = self.send_message(nodes[node], endpoint, payload)
            if result:
                results[node] = result

    def run(self, node):
        for network_function in self.network_functions:
            self.network_functions[network_function].run(node)
        Thread(target=lambda: self.app.run(host='0.0.0.0', port=self.port)).start()
