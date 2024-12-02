from distributed_environment_builder.infrastructure.hii.hii import Hii


class CpuInstruction(Hii):

    def __init__(self, time, util):
        self.consumed_time = 0
        self.consumed_units = 0
        self.time = time
        self.util = util
        self.capacity = 10

    def compute(self, payload: float):
        self.consumed_time = self.consumed_time + self.time(payload)
        self.consumed_units = self.consumed_units + self.util(payload)

    def get_time(self):
        return self.consumed_time

    def get_utilization(self, time):
        return self.consumed_units / (self.capacity * time)

