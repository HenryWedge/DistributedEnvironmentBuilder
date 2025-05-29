from distributed_environment_builder.benchmark.new.event_location_mapper import EventLocationMapper
from distributed_environment_builder.benchmark.new.infrastructure import Infrastructure
from distributed_environment_builder.benchmark.new.load_generator import LoadGenerator
from distributed_environment_builder.benchmark.new.monitor import Monitor

class Benchmark:
    def __init__(
            self,
            load_generator,
            request_generator,
            event_location_mapper,
            infrastructure,
            monitor,
            experiment_duration
    ):
        self.load_generator: LoadGenerator = load_generator
        self.request_generator = request_generator
        self.event_location_mapper: EventLocationMapper = event_location_mapper
        self.infrastructure: Infrastructure = infrastructure
        self.monitor: Monitor = monitor
        self.experiment_duration = experiment_duration

    def run_experiment(self):
        for i in range(self.experiment_duration):
            event = self.load_generator.next_event()
            event_location = self.event_location_mapper.get_location(event)
            self.infrastructure.receive_event(event_location, event)
            if not self.monitor.monitor():
                return False
