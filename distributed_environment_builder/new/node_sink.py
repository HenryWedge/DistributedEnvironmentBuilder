from distributed_event_factory.provider.sink.sink_provider import Sink
from process_mining_core.datastructure.core.event import Event

class NodeSink(Sink):

    def __init__(self, node, data_source_ref):
        super().__init__(data_source_ref)
        self.node = node
        self.i = 0

    def send(self, event: Event) -> None:
        self.i = self.i+1

        if self.i < 50:
            self.node.network.send_message(event.group, "event", event)
        else:
            self.print_conformace_score(self.node.network.send_message(event.group, "conformance", event))
        #print(self.node.network.send_message(event.group, "dfg", None))
        #print(f"Utilization: {self.node.get_storage_utilization()}")

    def print_conformace_score(self, conf):
        if conf.path_length:
            print(f"Conformance: {1 - (conf.conformance_violations / conf.path_length)}")
        else:
            print(f"Conformance: {0.0}")

    def get_datasource_ref(self):
        return super().get_datasource_ref()