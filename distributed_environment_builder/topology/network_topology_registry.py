from distributed_environment_builder.topology.network_topology_impl import NetworkTopologyImpl

network_dict = dict()

def get_network_topology(name):
    if not name in network_dict:
        network_dict[name] = NetworkTopologyImpl()
    return network_dict[name]
