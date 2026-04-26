# https://leetcode.com/problems/unique-paths/?envType=problem-list-v2&envId=dynamic-programming
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        f_row = [1] * n
        s_row = [1] * n
        for _ in range(m - 1):
            for i, val in enumerate(f_row):
                if i == 0:
                    s_row[i] = val
                else:
                    s_row[i] = val + s_row[i - 1]
            print(f_row)
            print(s_row)
            f_row, s_row = s_row, f_row
        return f_row[-1]
