from distributed_environment_builder.infrastructure.hii.hii import Hii

class NetworkInstruction(Hii):

    def __init__(self, time, util, capacity):
        self.consumed_time = 0
        self.consumed_units = 0
        self.time = time
        self.util = util
        self.capacity = capacity

    def send(self, payload: float):
        self.consumed_time = self.consumed_time + self.time(payload)
        self.consumed_units =self.consumed_units + self.util(payload)

    def get_time(self):
        return self.consumed_time

    def get_utilization(self, time):
        return self.consumed_units / (self.capacity * time)

    def adjust_capacity(self, new_capacity):
        self.capacity = new_capacity

    def reset(self):
        self.consumed_time = 0
        self.consumed_units = 0

