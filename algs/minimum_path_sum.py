# https://leetcode.com/problems/minimum-path-sum/description/


class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        f_row = [None] * len(grid[0])
        s_row = [None] * len(grid[0])

        f_row[0] = grid[0][0]
        for i in range(1, len(grid[0])):
            f_row[i] = f_row[i - 1] + grid[0][i]
        # print()

        # print(f_row)
        # print(s_row)

        for m in range(1, len(grid)):
            for n in range(len(grid[0])):
                if n == 0:
                    s_row[0] = f_row[n] + grid[m][n]
                else:
                    # print(f"grid[{m}][{n}]" ,grid[m][n])
                    s_row[n] = min(s_row[n - 1], f_row[n]) + grid[m][n]
            # print()
            # print(f_row)
            # print(s_row)
            f_row = s_row
            s_row = [None] * len(grid[0])

        return f_row[-1]
