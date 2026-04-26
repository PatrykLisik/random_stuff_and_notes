# https://leetcode.com/problems/longest-valid-parentheses/?envType=problem-list-v2&envId=dynamic-programming

class Solution:
    def longestValidParentheses(self, s: str) -> int:
        # this chesse do not work because of this:
        # "()(()"
        # do not know if 3rd ( is valid and we must assume it is 
        l_count = 0
        r_count = 0
        longest = 0
        curr = 0
        for ss in s:
            if ss == "(":
                l_count += 1
            if ss == ")":
                r_count += 1
            # matched
            print(f"{l_count=} {r_count=}")
            if l_count > 0 and r_count > 0:
                curr += 2
                l_count -= 1
                r_count -= 1
                longest = max(curr, longest)
            if l_count == 0 and r_count == 1:
                curr = 0
                r_count = 0
        return longest
