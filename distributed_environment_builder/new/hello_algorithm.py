from compute.my_compute import MyCompute
from network.fw.network import Network
from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph
from storage.dcc_storage import DccStorage

class SayHelloAlgorithm:

    def __init__(self):
        self.node_id = None

    def run_on_node(self, node):
        self.node_id: str = node.node_id
        self.storage: DccStorage = DccStorage(node.storage)
        self.cpu = MyCompute()
        self.network: Network = node.network
        self.network.add_network_function("event", self.process_event, Event)
        self.network.add_network_function("timestamp", self.get_timestamp_of_case, str)
        self.network.add_network_function("conformance", self.get_conformance_of_case, None)
        self.network.add_network_function("dfg", self.get_directly_follows_graph, None)

    def process_event(self, event):
        print(event)
        activity = event.activity
        last_event: Event = self.storage.get_activity_of_case(event.caseid)

        node_with_timestamp = self.network.broadcast(endpoint="timestamp", payload=event.caseid)

        predecessor_node = self.cpu.get_predecessor_node(last_event, node_with_timestamp)
        self.storage.store_event_for_case(event)

        predecessor = None
        if predecessor_node:
            self.storage.store_start_activity(event.activity)
            predecessor = predecessor_node
        elif last_event:
            predecessor = last_event.activity

        if predecessor:
            self.storage.store_directly_follows_relation(
                DirectlyFollowsRelation(
                    predecessor=predecessor,
                    successor=activity
                )
            )
        self.storage.update_last_event_of_case(event.caseid, event.activity)
        return ""

    def get_timestamp_of_case(self, case_id):
        last_event: Event = self.storage.get_activity_of_case(case_id)
        if last_event:
            last_timestamp = last_event.timestamp
            return last_timestamp
        return None

    def get_conformance_of_case(self, event):
        conformance_values = self.storage.retrieve_conformance_values(event.caseid)
        dfg: DirectlyFollowsGraph = self.storage.get_directly_follows_graph()
        conformance = self.cpu.compute_conformance(dfg, conformance_values, event.activity)
        self.storage.update_conformance(event.caseid, conformance)
        return conformance

    def get_directly_follows_graph(self, payload):
        return self.storage.get_directly_follows_graph()