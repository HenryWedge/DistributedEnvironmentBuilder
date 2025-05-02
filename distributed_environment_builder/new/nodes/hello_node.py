from threading import Thread

from flask import Flask

from nodes.node_interface import NodeInterface

class HelloNode(NodeInterface):

    def __init__(self, node_id, port, network, storage):
        self.node_id = node_id
        self.app = Flask(f"{self.node_id}")
        self.endpoints = dict()
        self.port = port
        self.network = network
        self.storage = storage

    def run(self):
        self.network.run(self)
        Thread(target=lambda: self.app.run(host='0.0.0.0', port=self.port)).start()