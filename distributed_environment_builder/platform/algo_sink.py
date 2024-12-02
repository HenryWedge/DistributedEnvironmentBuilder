from distributed_environment_builder.algo.dfgminer.dfg_miner import DfgMiner
from distributed_event_factory.provider.sink.sink_provider import Sink
from process_mining_core.datastructure.core.event import Event


class DfgMinerAlgoSink(Sink):
    def __init__(self,
                 data_source_ref,
                 miner):
        super().__init__(data_source_ref)
        self.dfg_algo: DfgMiner = miner

    def send(self, event: Event) -> None:
        self.dfg_algo.receive_event(event)
