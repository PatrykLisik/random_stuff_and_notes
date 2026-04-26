class Solution:
    def search(self, nums: list[int], target: int) -> int:
        # find rotation point
        l = 0
        r = len(nums) - 1
        while l <= r:
            mid = (r + l) // 2
            if nums[0] <= nums[mid]:
                l = mid + 1
            else:
                r = mid - 1

        # b search each part
        def b_search(nums2: list[int], target: int) -> int:
            l1 = 0
            r1 = len(nums2) - 1
            while l1 <= r1:
                mid = (l1 + r1) // 2
                if nums2[mid] == target:
                    return mid
                if nums2[mid] < target:
                    l1 = mid + 1
                else:
                    r1 = mid - 1
            return -1

        print(l)

        ret = b_search(nums[:l], target)
        if ret != -1:
            return ret
        ret = b_search(nums[l:], target)
        if ret != -1:
            return ret + l
        return -1
