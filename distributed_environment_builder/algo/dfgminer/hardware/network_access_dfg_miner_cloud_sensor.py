from distributed_environment_builder.algo.dfgminer.hardware.network_dfg_miner import Network


class NetworkAccessDfgMinerCloudSensor:

    def __init__(self, node_id, network, topology):
        self.network = network
        self.node_id = node_id
        self.topology: Network = topology

    def send_event(self, event) -> None:
        for node in self.topology.get_all_cloud_nodes(self.node_id):
            self.network.send(payload=1)
            node.receive_event(event)