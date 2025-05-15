from my_compute import MyCompute
from process_mining_core.datastructure.core.counted_directly_follows_relation import CountedDirectlyFollowsRelation
from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph


class MyTestCase():

    def get_dfg(self):
        relations = CountedDirectlyFollowsRelation(dict())

        relations.insert(DirectlyFollowsRelation("A", "B"))
        relations.insert(DirectlyFollowsRelation("B", "B"))
        relations.insert(DirectlyFollowsRelation("B", "C"))
        relations.insert(DirectlyFollowsRelation("C", "D"))
        relations.insert(DirectlyFollowsRelation("B", "E"))
        relations.insert(DirectlyFollowsRelation("D", "F"))

        return DirectlyFollowsGraph(
            relations,
            ["A"],
            ["E", "F"]
        )

    def test_something(self):
        testee = MyCompute()
        print(testee.get_path_to_activity(self.get_dfg(), "B", "B"))

    def test_conformance(self):
        testee = MyCompute()
        dfg = self.get_dfg()
        print(testee.compute_conformance(dfg, "A", "C"))

if __name__ == '__main__':
    MyTestCase().test_something()
