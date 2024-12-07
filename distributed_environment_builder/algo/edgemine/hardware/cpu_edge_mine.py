from distributed_environment_builder.infrastructure.hii.cpu_hii import CpuInstruction
from process_mining_core.datastructure.converter.directly_follows_graph_merger import DirectlyFollowsGraphMerger
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph


class EdgeMineCpu:

    def __init__(self, cpu: CpuInstruction):
        self.cpu = cpu

    def merge_dfgs(self, dfg1: DirectlyFollowsGraph, dfg2: DirectlyFollowsGraph):
        #self.cpu.compute(len(dfg1.relations) + len(dfg2.relations))
        self.cpu.compute(1)
        return DirectlyFollowsGraphMerger().merge_directly_follows_graph(dfg1, dfg2)
