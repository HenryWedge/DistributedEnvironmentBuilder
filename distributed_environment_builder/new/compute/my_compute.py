import heapq

from process_mining_core.datastructure.core.model.directly_follows_graph import DirectlyFollowsGraph


class MyCompute:

    def get_predecessor_node(self, last_event, nodes_with_timestamp_of_latest_event):
        if last_event:
            latest_timestamp = last_event.timestamp
        else:
            latest_timestamp = None

        predecessor_node = None
        if nodes_with_timestamp_of_latest_event:
            for node in nodes_with_timestamp_of_latest_event:
                timestamp = nodes_with_timestamp_of_latest_event[node]
                if not latest_timestamp or timestamp > latest_timestamp:
                    latest_timestamp = timestamp
                    predecessor_node = node
        return predecessor_node

    def compute_conformance(self, directly_follows_graph: DirectlyFollowsGraph, current_activity, next_activity):
        conformance_violations = 0
        if not self.has_item(directly_follows_graph, next_activity):
            conformance_violations = conformance_violations + 1
        else:
            for dfr in directly_follows_graph.get_relations():
                if dfr.predecessor == current_activity:
                    if next_activity in self.get_neighbours(directly_follows_graph, current_activity):
                        current_activity = next_activity
                    else:
                        conformance_violations = conformance_violations + \
                                                 len(self.get_path_to_activity(directly_follows_graph, current_activity,
                                                                               next_activity)) - 2

        if not directly_follows_graph.start_activities:
            print("Help!!!!")
            return 0
        else:
            print("Start activities")
            print(directly_follows_graph.start_activities)

        shortest_path = self.get_path_to_activity(
            directly_follows_graph,
            list(directly_follows_graph.start_activities)[0],
            next_activity
        )
        if not shortest_path or len(shortest_path) == 1:
            return 1 - conformance_violations
        else:
            return 1 - (conformance_violations / (len(shortest_path) - 1))

    def has_item(self, directly_follows_graph: DirectlyFollowsGraph, item):
        for dfr in directly_follows_graph.get_relations():
            if dfr.predecessor == item or dfr.successor == item:
                return True
        return False

    def get_neighbours(self, dfg: DirectlyFollowsGraph, pointer):
        neighbours = []
        for relation in dfg.get_relations():
            if relation.predecessor == pointer:
                neighbours.append(relation.successor)
        return neighbours

    def get_path_to_activity(self, dfg, pointer, target):
        if not self.has_item(dfg, pointer) or not self.has_item(dfg, target):
            return None  # One or both edges don't exist in the graph

        distances = {pointer: 0}
        priority_queue = [(0, pointer, [])]  # (distance, current_edge, path)

        while priority_queue:
            current_distance, current_edge, path = heapq.heappop(priority_queue)

            if current_edge == target:
                return path + [current_edge]

            if current_distance > distances.get(current_edge, float('inf')):
                continue

            for neighbor_edge in self.get_neighbours(dfg, current_edge):
                distance = current_distance + 1
                if distance < distances.get(neighbor_edge, float('inf')):
                    distances[neighbor_edge] = distance
                    heapq.heappush(priority_queue, (distance, neighbor_edge, path + [current_edge]))
        return None
