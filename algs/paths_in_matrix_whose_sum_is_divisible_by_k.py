class Solution:
    def numberOfPaths(self, grid: list[list[int]], k: int) -> int:
        big_prime = 10**9 + 7
        # array `[0] * k` stores counts of reminders
        # [1,2,0,0] means 1 0-reminder, two  1-remindres etc
        # we only condier two rows as storing the rest is redundant
        f_row = [[0] * k for _ in range(len(grid[0]))]  # first row
        s_row = [[0] * k for _ in range(len(grid[0]))]  # second row

        rem = grid[0][0] % k
        f_row[0][rem] = 1
        # print(f_row)
        for i in range(1, len(grid[0])):
            for rem_val, rem_count in enumerate(f_row[i - 1]):
                rem = (rem_val + grid[0][i]) % k
                f_row[i][rem] += rem_count
        # print(f_row)
        for m in range(1, len(grid)):
            for n in range(len(grid[0])):
                # top reminders
                for rem_val, rem_count in enumerate(f_row[n]):
                    rem = (rem_val + grid[m][n]) % k
                    # print(rem)
                    s_row[n][rem] += rem_count
                    s_row[n][rem] %= big_prime
                # left reminders
                if n > 0:
                    for rem_val, rem_count in enumerate(s_row[n - 1]):
                        rem = (rem_val + grid[m][n]) % k
                        s_row[n][rem] += rem_count
                        s_row[n][rem] %= big_prime
            # print(f_row)
            # print(s_row)
            f_row = s_row
            s_row = [[0] * k for _ in range(len(grid[0]))]
        # print(f_row)
        return f_row[-1][0]
