class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        nums_cache = {n: i for  i,n in enumerate(nums)}
        
        for i,n in enumerate(nums):
            index = nums_cache.get(target - n)
            if index is not None and i!=index:
                return [i, index]
