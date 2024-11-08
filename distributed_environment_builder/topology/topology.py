from typing import List

from DistributedEnvironmentBuilder.distributed_environment_builder.hardware.network import Network
from distributed_environment_builder.algo.baseline.impl.edgenode import EdgeNode


class Topology:

    def __init__(self):
        self.nodes: List[EdgeNode] = []
        self.network: List[Network] = []

    def add_node(self, node: EdgeNode):
        self.nodes.append(node)

