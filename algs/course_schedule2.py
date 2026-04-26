class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        prerequisite_per_i = [[] for _ in range(numCourses)]
        pass_cache = [None] * numCourses
        for idx, pre in prerequisites:
            prerequisite_per_i[idx].append(pre)

        def get_pre(i, v: set | None = None):
            if v is None:
                v = set()

            if i in v:
                raise ValueError
            v.add(i)

            if pass_cache[i] is True:
                return []

            ret = []
            for pre in prerequisite_per_i[i]:
                ret.extend(get_pre(pre, v))
            if pass_cache[i] is None:
                ret.append(i)
                pass_cache[i] = True
            return ret

        order = []
        try:
            for i in range(numCourses):
                order.extend(get_pre(i))
            return order
        except ValueError:
            return []
