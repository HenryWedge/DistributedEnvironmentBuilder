import asyncio
import time
from abc import ABC
from threading import Lock


class Compute(ABC):

    def __init__(self, operations_per_second):
        self.operations_per_second = operations_per_second
        self.queue = []
        self.mutex = Lock()

    def get_utilization(self):
        return len(self.queue) / self.operations_per_second

    async def submit(self, f):
        with self.mutex:
            self.queue.append(f)
        sleep_time = len(self.queue) / self.operations_per_second
        await asyncio.sleep(sleep_time)
        with self.mutex:
            self.queue.remove(f)
        return f()

