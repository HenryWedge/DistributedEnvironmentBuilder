from threading import Thread

import requests
from flask import Flask, request

from nodes.node_interface import NodeInterface


class HelloNode(NodeInterface):
    def __init__(self, node_id, network, storage):
        self.node_id = node_id
        self.app = Flask(f"{self.node_id}")
        self.endpoints = dict()
        self.network = network
        self.storage = storage
        network.add_node(self)

    def call_endpoint(self, endpoint, payload):
        return requests.post(url=f"http://localhost:{self.node_id}/{endpoint}", json=payload).content

    def register_endpoint(self, endpoint, func, methods=["GET", "POST"]):
        self.app.add_url_rule(
            f"/{endpoint}",
            methods=methods,
            endpoint=endpoint,
            view_func=lambda: func(request.get_json()),
        )

    def run(self):
        Thread(target=lambda: self.app.run(host='0.0.0.0', port=self.node_id)).start()