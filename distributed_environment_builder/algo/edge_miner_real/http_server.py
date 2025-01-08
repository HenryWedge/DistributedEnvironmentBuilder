from threading import Thread

import requests
from flask import Flask, request

def lol(func):
    def wrapper(self, *args, **kwargs):
        print("Before method execution")
        res = func(self, *args, **kwargs)
        print("After method execution")
        return res
    return wrapper

class Network:
    def __init__(self):
        self.all_nodes = dict()

    def add_node(self, node_id: str) -> None:
        self.all_nodes[node_id] = CounterProxy(node_id)

    def get_all_nodes(self, own_node_id: str):
        return [self.all_nodes[node] for node in self.all_nodes if node != own_node_id]

class CountNode:
    def __init__(self, own_node_id, network: Network):
        self.c = 0
        self.own_node_id = own_node_id
        self.network = network

    @lol
    def count(self, i: int):
        self.c = self.c + i
        return self.c

    def global_count(self):
        total_count = 0
        for node in self.network.get_all_nodes(self.own_node_id):
            total_count = total_count + node.count()
        return total_count

class GenericProxy:
    def __init__(self, name):
        self.name = name

    def get(self):
        return requests.get(url=f"http://localhost:{self.node_id}/{self.name}").json()

class CounterProxy:
    def __init__(self, node_id):
        self.node_id = node_id

    def count(self):
        return requests.get(url=f"http://localhost:{self.node_id}/count").json()

class CounterEndpoint:
    def __init__(self, count_node):
        self.count_node: CountNode = count_node

    @lol
    def count(self):
        i = request.args.get("i")
        if i:
            i = int(i)
        else:
            i = 0
        return f"{self.count_node.count(i)}"

    def global_count(self):
        return f"{self.count_node.global_count()}"

class Counter:
    def __init__(self, node_id, endpoint):
        self.c = 0
        self.node_id = node_id
        self.endpoint = endpoint
        self.app = Flask(f"{self.node_id}")

    def run(self):
        self.app.add_url_rule("/count", methods=["GET"], view_func=self.endpoint.count)
        self.app.add_url_rule("/countg", methods=["GET"], view_func=self.endpoint.global_count)
        self.app.run(host='0.0.0.0', port=self.node_id)

class EndpointDefinition:

    def __init__(self, name, function, args):
        self.name = name
        self.function = function
        self.args = args

    def get_counter_proxy(self):
        return GenericProxy(self.name)


if __name__ == '__main__':
    network = Network()
    network.add_node("5000")
    network.add_node("5001")

    count_node = CountNode("5000", network)
    endpoint_definitions = [EndpointDefinition("count", count_node.count, {})]


    getattr(count_node, "count").decorator

    #for definition in endpoint_definitions:
    #    print(getattr(definition, "count"))

    #counter  = Counter(5000, CounterEndpoint(CountNode(5000, network)))
    #counter2 = Counter(5001, CounterEndpoint(CountNode(5001, network)))
#
    #t1 = Thread(target=counter.run)
    #t2 = Thread(target=counter2.run)
#
    #t1.start()
    #t2.start()
