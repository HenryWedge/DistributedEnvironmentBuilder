from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event
from storage.case_actity_tuple import CaseActivityTuple
from storage.dcc_storage import DccStorage

class SayHelloAlgorithm:

    def __init__(self):
        self.node_id = None

    def run_on_node(self, node):
        self.node_id = node.node_id
        self.storage: DccStorage = DccStorage(node.storage)
        self.network = node.network
        node.network.add_network_function("event", self.process_event, Event)
        node.network.add_network_function("conformance", self.get_conformance_of_case, None)

    def process_event(self, event):
        activity = event.activity
        last_activity = self.storage.get_activity_of_case(event.caseid)
        self.storage.store_last_event_of_case(
            CaseActivityTuple(
                case=event.caseid,
                activity=event.activity
            )
        )

        if last_activity:
            self.storage.store_directly_follows_relation(
                DirectlyFollowsRelation(
                    predecessor=last_activity,
                    successor=activity
                )
            )

        print(event)
        return ""

    def get_conformance_of_case(self, payload):
        pass
