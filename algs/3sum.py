# https://leetcode.com/problems/3sum/


class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        resp = []
        nums_cache = {v: i for i, v in enumerate(nums)}

        for i, n in enumerate(nums):
            for j, k in enumerate(nums):
                if i == j:
                    continue
                third_num = -(n + k)
                third_num_idx = nums_cache.get(third_num)
                if (
                    third_num_idx is not None
                    and third_num_idx != i
                    and third_num_idx != j
                ):
                    resp.append([n, k, third_num])
        return resp
