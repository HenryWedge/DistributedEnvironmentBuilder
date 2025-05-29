from threading import Thread
import requests
from flask import Flask

class AlgoNetwork:
    def __init__(self):
        self.participants = dict()

    def get_participants_with_label(self, label):
        return self.participants.get(label)

    def register(self, participant, label):
        participant.add_network(network=self)
        self.participants[label] = participant

class Algo:
    def __init__(self):
        self.network = None

    def add_network(self, network):
        self.network = network
        print("debug")

    def receive_event(self):
        for participant in self.network.get_participants_with_label("label1"):
            info = participant.get_information()
            print(info)

    def get_information(self):
        return "Du bist sweet"

class NetworkedAlgo:
    def __init__(self, id, algo):
        self.algo = algo
        self.id = id
        app = Flask(id)
        app.add_url_rule("/info", methods=["GET"], view_func=self.algo.get_information)
        app.add_url_rule("/event", methods=["GET"], view_func=self.algo.receive_event)
        Thread(target=lambda: app.run(host="0.0.0.0", port=self.id)).start()

    def get_information(self):
        requests.get(url=f"http://localhost:{self.id}/info").json()

if __name__ == '__main__':
    algo1 = Algo()
    algo2 = Algo()
    network = AlgoNetwork()
    network.register(algo1, "label1")
    network.register(algo2, "label1")
    NetworkedAlgo(id = "5000", algo=Algo())
    NetworkedAlgo(id = "5001", algo=Algo())