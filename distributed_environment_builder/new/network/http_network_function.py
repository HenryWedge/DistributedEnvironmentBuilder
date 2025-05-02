import requests
from flask import request

from network.fw.network_function import NetworkFunction

class HttpNetworkFunction(NetworkFunction):

    def __init__(self, app, endpoint, methods, func):
        self.app = app
        self.endpoint = endpoint
        self.methods = methods
        self.func = func

    def call(self, payload):
        requests.post(url=f"http://localhost:{self.node_id}/{self.endpoint}", json=payload).content

    def run(self):
        self.app.add_url_rule(
            f"/{self.endpoint}",
            methods=self.methods,
            endpoint=self.endpoint,
            view_func=lambda: self.func(request.get_json()),
        )