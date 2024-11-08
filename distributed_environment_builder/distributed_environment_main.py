from distributed_environment_builder.algo.baseline.impl.centralnode import CentralNode
from distributed_environment_builder.dataconnector.baseline.central.baseline_dfg_miner_parser import \
    BaselineDfgMinerCentralParser
from distributed_environment_builder.dataconnector.baseline.central.baseline_dfg_miner_sink import \
    BaselineDfgMinerCentralNode
from distributed_environment_builder.dataconnector.baseline.edge.baseline_dfg_miner_parser import BaselineDfgMinerParser
from distributed_environment_builder.dataconnector.baseline.edge.baseline_dfg_miner_sink import BaselineDfgMinerSink
from distributed_environment_builder.topology.network_topology_registry import get_network_topology
from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':
    event_factory: EventFactory = (EventFactory()
     .add_sink_parser(key="dfgMiner", parser=BaselineDfgMinerParser())
     .add_sink_parser(key="centralDfgMiner", parser=BaselineDfgMinerCentralParser())
     .add_directory(directory="../../DistributedEventFactory/config/datasource/assemblyline")
     .add_file(filename="../../DistributedEventFactory/config/simulation/countbased.yaml")
     .add_directory(directory="../config/sinks"))

    nodes = [
        ("GoodsDelivery","net0"),
        ("MaterialPreparation","net1"),
        ("AssemblyLineSetup","net2"),
        ("Assembling","net3"),
        ("QualityControl","net3"),
        ("Packing","net4"),
        ("Shipping","net4")
    ]
    for i in range(len(nodes)):
        node = nodes[i]
        event_factory.add_sink(
            f"node{i}",
            BaselineDfgMinerSink(
                data_source_ref=[node[0]],
                network_ref=node[1],
                sender_id=f"node{i}"
            )
        )

    for i in range(5):
        event_factory.add_sink(
            f"central-{i}",
            BaselineDfgMinerCentralNode(
                data_source_ref=[],
                network_ref=f"net{i}",
                sender_id=f"central-{i}"
            )
        )
    central_node: CentralNode = event_factory.sinks["central-0"]
    event_factory.run(
        hook=lambda: print(
        f"Total: {get_network_topology('net0').get_used_bandwidth() + get_network_topology('net1').get_used_bandwidth() + get_network_topology('net2').get_used_bandwidth()}, "
        f"Net1: {get_network_topology('net0').get_used_bandwidth()}, " +
        f"Net2: {get_network_topology('net1').get_used_bandwidth()}",
        f"Net3: {get_network_topology('net2').get_used_bandwidth()}",
        f"DFG: {central_node.processing_node.get_directly_follows_graph()}"))

