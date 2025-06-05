from typing import List, Any


class NodeMonitor:

    def __init__(self):
        self.metrics = dict()

    def add_value(self, metric, value):
        if metric in self.metrics:
            self.metrics[metric].append(value)
        else:
            self.metrics[metric] = [value]

    def get_metric(self, name) -> List[Any]:
        return self.metrics[name]