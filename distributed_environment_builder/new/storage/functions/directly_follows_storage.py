from abc import ABC

from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph


class DirectlyFollowsStorage(ABC):

    def get_directly_follows_graph(self):
        pass

    def store_directly_follows_relation(self, directly_follows_relation):
        pass