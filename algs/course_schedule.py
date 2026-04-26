# https://leetcode.com/problems/course-schedule


class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        pass_cache: list[bool | None] = [None] * numCourses
        prerequisite_per_i = [[] for _ in range(numCourses)]
        for idx, pre in prerequisites:
            prerequisite_per_i[idx].append(pre)

        def can_be_passed(i, visited: set | None = None):
            if visited is None:
                visited = set()

            if pass_cache[i] is not None:
                return pass_cache[i]

            if len(prerequisite_per_i[i]) == 0:
                pass_cache[i] = True
                return True

            if i in visited:
                return False
            visited.add(i)

            for prereq in prerequisite_per_i[i]:
                if can_be_passed(prereq, visited=visited) is False:
                    return False
            pass_cache[i] = True
            return True

        for i in range(numCourses):
            if can_be_passed(i) is False:
                return False
        return True
