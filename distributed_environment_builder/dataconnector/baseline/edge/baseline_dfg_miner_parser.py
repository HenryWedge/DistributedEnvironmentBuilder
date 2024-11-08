from distributed_environment_builder.dataconnector.baseline.edge.baseline_dfg_miner_sink import BaselineDfgMinerSink
from distributed_event_factory.parser.sink.sink_parser import SinkParser

class BaselineDfgMinerParser(SinkParser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config) -> BaselineDfgMinerSink:
        return BaselineDfgMinerSink(
            sender_id=config["senderId"],
            data_source_ref=config["dataSourceRefs"],
            network_ref=config["network"]
        )
