from compute.compute import Compute
from process_mining_core.datastructure.converter.heuristics_net_petri_net_converter import \
    HeuristicsNetPetriNetConverter


class MyCompute(Compute):

    def create_petrinet(self, payload):
        HeuristicsNetPetriNetConverter().create_petri_net()