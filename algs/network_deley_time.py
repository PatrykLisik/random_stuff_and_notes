# https://leetcode.com/problems/network-delay-time


from heapq import heappop, heappush
import math


class Solution:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        # g[node_idx] = [(target_node, weight),(target_node, weight)]
        graph = [[] for _ in range(n + 1)]
        min_time_for_node = [math.inf for _ in range(n + 1)]
        visited = set()
        for min_time_for_node in times:
            graph[min_time_for_node[0]].append((min_time_for_node[1], min_time_for_node[2]))
        que = []
        heappush(que, (0, k))
        while len(que) > 0:
            p, node = heappop(que)
            min_time_for_node[node] = min(p, min_time_for_node[node])
            for next_node, w in graph[node]:
                heappush(que, ((p + w), next_node))
            visited.
        return max(min_time_for_node)
