import requests
from flask import request

from network.fw.network_function import NetworkFunction
from process_mining_core.datastructure.core.event import Event


class HttpNetworkFunction(NetworkFunction):

    def __init__(self, app, func, endpoint, clazz):
        self.app = app
        self.func = func
        self.endpoint = endpoint
        self.clazz = clazz

    def call(self, address, endpoint, payload):
        return requests.post(url=f"http://{address}/{endpoint}", json=payload.__dict__).content

    def run(self, node):
        self.app.add_url_rule(
            f"/{self.endpoint}",
            methods=["GET", "POST"],
            endpoint=self.endpoint,
            view_func=lambda: self.func(event=self.clazz.from_dict(request.get_json())),
        )
