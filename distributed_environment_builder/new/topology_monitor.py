from node_monitor import NodeMonitor

class TopologyMonitor:

    def __init__(self):
        self.nodes = dict()

    def add_node(self, name):
        node_monitor = NodeMonitor()
        self.nodes[name] = node_monitor
        return node_monitor

    def get_node_monitor(self, name) -> NodeMonitor:
        return self.nodes[name]
