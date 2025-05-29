from process_mining_core.datastructure.core.directly_follows_relation import DirectlyFollowsRelation
from file_storage import DictFileStorage

s = DictFileStorage(filepath="../G1-df")
dfr = DirectlyFollowsRelation("G7", "Reject")

print(hash(dfr))
print("---")
for i in s._data:
    print(hash(DirectlyFollowsRelation.from_string(i)))