from distributed_environment_builder.dataconnector.baseline.central.baseline_dfg_miner_sink import \
    BaselineDfgMinerCentralNode
from distributed_event_factory.parser.sink.sink_parser import SinkParser

class BaselineDfgMinerCentralParser(SinkParser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config) -> BaselineDfgMinerCentralNode:
        return BaselineDfgMinerCentralNode(
            sender_id=config["senderId"],
            data_source_ref=None,
            network_ref=config["network"]
        )
