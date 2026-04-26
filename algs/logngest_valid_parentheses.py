# https://leetcode.com/problems/longest-valid-parentheses/?envType=problem-list-v2&envId=dynamic-programming


class Solution:
    def find_r_(self, s, pos):
        l, r = pos
        if r + 2 < len(s) and s[r + 1] == "(" and s[r + 2] == ")":
            # print(f"FIND r found,", l, r + 2)
            return l, r + 2

    def find_l_(self, s, pos):
        l, r = pos
        if l - 2 >= 0 and s[l - 2] == "(" and s[l - 1] == ")":
            # print(f"FIND l found,", l - 2, r)
            return l - 2, r

    def find_b_(self, s, pos):
        # print(f"FIND b,", pos, len(s))
        l, r = pos
        if l - 1 >= 0 and r + 1 < len(s) and s[l - 1] == "(" and s[r + 1] == ")":
            print(f"FIND b found,", l - 1, r + 1)
            # print(self.valid)
            return l - 1, r + 1

    def add_to_q(self, new_pos, s):
        # print(self.valid)
        # print("add pos", new_pos)
        le, re = new_pos
        lh = re - le + 1
        if self.valid[re] > lh:
            # print("ignore")
            return None
        if le - 1 > 0 and self.valid[le - 1] > 0:
            # print("left touch", le - 1)
            le = le - self.valid[le - 1]
            touch = True
        if re + 1 < len(s) and self.valid[re + 1] > 0:
            # print("righ touch", re + 1)
            touch = True
            re = re + self.valid[re + 1]

        lh = re - le + 1
        for p in range(le, re):
            self.valid[p] = lh
        self.longest = max(lh, self.longest)
        new_pos = (le, re)
        # print("adding pos", new_pos)
        self.q.append(new_pos)

    def longestValidParentheses(self, s: str) -> int:
        # () -> ()()
        # () -> (())
        # )( bad
        self.q = []
        self.valid = [0] * len(s)
        self.longest = 0
        for i in range(len(s) - 1):
            if s[i] == "(" and s[i + 1] == ")":
                self.add_to_q((i, i + 1), s)
        # print(q)
        while self.q:
            pos = self.q.pop()
            new_pos = (
                self.find_b_(s, pos) or self.find_l_(s, pos) or self.find_r_(s, pos)
            )
            if new_pos:
                self.add_to_q(new_pos=new_pos, s=s)
        # print(self.valid)
        return self.longest
