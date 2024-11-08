from distributed_environment_builder.algo.baseline.interface.central_node_interface import CentralNodeInterface
from distributed_environment_builder.topology.network_topology_interface import NetworkTopology
from process_mining_core.datastructure.converter.directly_follows_graph_merger import DirectlyFollowsGraphMerger
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph

class CentralNode(CentralNodeInterface):

    def __init__(
            self,
            sender_id: str,
            network_topology: NetworkTopology
    ):
        self.sender_id = sender_id
        self.network_topology: NetworkTopology = network_topology

    def get_directly_follows_graph(self) -> DirectlyFollowsGraph:
        resulting_directly_follows_graph = None
        for receiver in self.network_topology.send_edge_nodes(self.sender_id):
            resulting_directly_follows_graph = self.merge_sub_dfgs(receiver, resulting_directly_follows_graph)
        for receiver in self.network_topology.send_central_nodes(self.sender_id):
            resulting_directly_follows_graph = self.merge_sub_dfgs(receiver, resulting_directly_follows_graph)
        return resulting_directly_follows_graph

    def merge_sub_dfgs(self, receiver, resulting_directly_follows_graph):
        dfg = receiver.get_directly_follows_graph()
        if not resulting_directly_follows_graph:
            resulting_directly_follows_graph = dfg
        else:
            resulting_directly_follows_graph = (DirectlyFollowsGraphMerger()
                                                .merge_directly_follows_graph(dfg, resulting_directly_follows_graph))
        return resulting_directly_follows_graph