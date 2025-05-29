from distributed_environment_builder.benchmark.event_emitter import EventEmitter
from distributed_event_factory.simulation.process_simulation import DefProcessSimulator
from process_mining_core.datastructure.core.event import Event

class DefEventEmitter(EventEmitter):

    def __init__(self, process_simulator: DefProcessSimulator):
        self.process_simulator: DefProcessSimulator = process_simulator

    def get_event(self) -> Event:
        return self.process_simulator.simulate()