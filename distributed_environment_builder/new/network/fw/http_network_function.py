import requests
from flask import request

from network.fw.network_function import NetworkFunction

class HttpNetworkFunction(NetworkFunction):

    def __init__(self, func, endpoint):
        self.func = func
        self.endpoint = endpoint

    def call(self, address, endpoint, payload):
        return requests.post(url=f"http://{address}/{endpoint}", json=payload).content

    def run(self, node):
        node.app.add_url_rule(
            f"/{self.endpoint}",
            methods=["GET", "POST"],
            endpoint=self.endpoint,
            view_func=lambda: self.func(request.get_json()),
        )