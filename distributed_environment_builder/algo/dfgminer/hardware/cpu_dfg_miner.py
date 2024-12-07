from typing import List, Dict, Any

from process_mining_core.datastructure.converter.directly_follows_graph_merger import DirectlyFollowsGraphMerger
from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.event import Event
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph

class CpuDfgMiner:
    def __init__(self, cpu):
        self.cpu = cpu

    def compute_largest_timestamp(self, events: List[Event]) -> Event:
        event_with_largest_timestamp = events[0]
        for event in events:
            if event is None:
                continue
            self.cpu.compute(payload=1)
            if event.timestamp > event_with_largest_timestamp.timestamp:
                event_with_largest_timestamp = event
        return event_with_largest_timestamp

    def build_dfg(self, directly_follows_relations: Dict[DirectlyFollowsRelation, int]) -> DirectlyFollowsGraph:
        counted_relations: Dict[tuple[Any, Any], int] = dict()
        for dfr in directly_follows_relations:
            self.cpu.compute(1)
            counted_relations[dfr.to_pair()] = directly_follows_relations[dfr]
        return DirectlyFollowsGraph(counted_relations, [], [])

    def merge_dfgs(self, dfg1: DirectlyFollowsGraph, dfg2: DirectlyFollowsGraph):
        self.cpu.compute(1)
        return DirectlyFollowsGraphMerger().merge_directly_follows_graph(dfg1, dfg2)
