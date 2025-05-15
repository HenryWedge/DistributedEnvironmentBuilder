from distributed_event_factory.provider.sink.sink_provider import Sink
from process_mining_core.datastructure.core.event import Event


class NodeSink(Sink):

    def __init__(self, node, data_source_ref):
        super().__init__(data_source_ref)
        self.node = node

    def send(self, event: Event) -> None:
        self.node.network.send_message(event.group, "event", event)
        print(self.node.network.send_message(event.group, "conformance", event).get_score())
        print(self.node.network.send_message(event.group, "dfg", None))

    def get_datasource_ref(self):
        return super().get_datasource_ref()