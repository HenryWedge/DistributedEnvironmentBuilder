import time

from compute.my_compute import MyCompute
from conformance_score import ConformanceScore
from hello_node import HelloNode
from network.fw.network import Network
from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph
from s_conformance_score import SConformanceScore
from storage.dcc_storage import DccStorage

class SayHelloAlgorithm:

    def __init__(self):
        self.node_id = None
        self.i = 0

    def run_on_node(self, node: HelloNode):
        self.node_id: str = node.node_id
        self.storage: DccStorage = DccStorage(node.get_storage("df"), node.get_storage("case"), node.get_storage("conform"))
        self.cpu = MyCompute(node.get_compute("cpu"))
        self.network: Network = node.control_network
        self.monitor = node.monitor

        self.network.add_network_function("event", self.process_event, Event)
        self.network.add_network_function("timestamp", self.get_timestamp_of_case, str)
        self.network.add_network_function("conformance", self.get_conformance_of_case, None)
        self.network.add_network_function("conformance_get", self.conformance_get, None)
        self.network.add_network_function("dfg", self.get_directly_follows_graph, None)

    def process_event(self, event):
        self.i = self.i + 1
        if self.i < 100:
            self.discover(event)
        else:
            self.get_conformance_of_case(event)
        return ""

    def discover(self, event):
        start = time.time()
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
        else:
            self.storage.store_start_activity(event.activity)

        if predecessor:
            self.storage.store_directly_follows_relation(
                DirectlyFollowsRelation(
                    predecessor=predecessor,
                    successor=activity
                )
            )
        end = time.time()
        self.monitor.add_value("discover_times", end-start)

    def get_timestamp_of_case(self, case_id):
        last_event: Event = self.storage.get_activity_of_case(case_id)
        if last_event:
            last_timestamp = last_event.timestamp
            return last_timestamp
        return None

    def get_conformance_of_case(self, event):
        start = time.time()
        conformance_values = self.storage.retrieve_conformance_values(event.caseid)

        last_activity = conformance_values.last_activity
        print(last_activity)
        dfg: DirectlyFollowsGraph = self.storage.get_directly_follows_graph()

        current_conformance = None
        if last_activity:
            print("Inner activity")
            current_conformance = ConformanceScore(conformance_values.conformance.path_length, conformance_values.conformance.conformance_violations)
        else:
            for node in dfg.get_predecessors_of_activity(event.activity):
                if self.network.has_node(node):
                    print("Inbound activity")
                    current_conformance = self.network.send_message(node, "conformance_get", event.caseid)
                    break
        if not current_conformance:
            print("Start activity")
            current_conformance = ConformanceScore(0, 0)

        conformance_update = self.cpu.compute_conformance(dfg, last_activity, event.activity)
        conformance = SConformanceScore(
            path_length=current_conformance.path_length + conformance_update.path_length,
            conformance_violations=current_conformance.conformance_violations + conformance_update.conformance_violations
        )
        self.storage.update_conformance(event.caseid, SConformanceScore(conformance_violations=conformance.conformance_violations, path_length=conformance.path_length))
        self.storage.update_last_event_of_case(event.caseid, event.activity)
        end = time.time()

        self.monitor.add_value("conformance_times", end - start)
        self.monitor.add_value("conformance", conformance)
        return conformance

    def conformance_get(self, case_id):
        return self.storage.retrieve_conformance_values(case_id).conformance

    def get_directly_follows_graph(self, payload):
        return self.storage.get_directly_follows_graph()