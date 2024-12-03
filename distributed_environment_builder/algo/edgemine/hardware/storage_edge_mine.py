from typing import Dict

from distributed_environment_builder.infrastructure.hii.storage_hii import StorageInstruction
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph

class EdgeMineStorage:
    def __init__(self, storage: StorageInstruction):
        self._most_frequent_predecessors: Dict[str, int] = dict()
        self._directly_follows_graph: DirectlyFollowsGraph = DirectlyFollowsGraph(counted_relations=dict())
        self._latest_event_per_case_id: Dict[str, str] = dict()
        self._case_successor: Dict[str, str] = dict()
        self.storage = storage

    def store_predecessor(self, predecessor):
        if predecessor in self._most_frequent_predecessors:
            self._most_frequent_predecessors[predecessor] = self._most_frequent_predecessors[predecessor] + 1
        else:
            self.storage.store(1)
            self._most_frequent_predecessors[predecessor] = 1

    def store_directly_follows_relation(self, directly_follows_relation):
        relations = self._directly_follows_graph.relations
        if directly_follows_relation in relations:
            relations[directly_follows_relation] = relations[directly_follows_relation] + 1
        else:
            self.storage.store(2)
            relations[directly_follows_relation] = 1

    def get_directly_follows_relations(self) -> DirectlyFollowsGraph:
        return self._directly_follows_graph

    def store_latest_event_for_case_id(self, case_id, event):
        if case_id not in self._latest_event_per_case_id:
            self.storage.store(1)

        self._latest_event_per_case_id[case_id] = event

    def store_case_successor(self, case_id, node_id):
        self.storage.store(1)
        self._case_successor[case_id] = node_id

    def get_latest_event_for_case(self, case_id):
        if case_id in self._latest_event_per_case_id:
            return self._latest_event_per_case_id[case_id]

    def get_most_frequent_predecessors(self):
        result = []
        for node_id in sorted(self._most_frequent_predecessors.items(), key=lambda item: item[1], reverse=True):
            result.append(node_id[0])
        return result