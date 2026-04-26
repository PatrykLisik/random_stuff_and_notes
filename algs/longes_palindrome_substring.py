class Solution:
    def _is_pal(self, s: str) -> bool:
        return s == s[::-1]

    def _l_around(self, s, l, h):

        if l>=1 and self._is_pal(s[l - 1 : h]):
            #print("left")
            return l - 1, h

        if h<len(s)+1 and self._is_pal(s[l : h + 1]):
            #print("right")
            return l, h + 1

        if l>=1 and h<len(s)+1 and self._is_pal(s[l - 1 : h + 1]):
            #print("both")
            return l - 1, h + 1
        return l, h

    def longestPalindrome(self, s: str) -> str:
        pal_que = [(i, i + 1) for i in range(len(s))][::-1]
        #pal_que = [(0,1)]
        res = 0, 1
        while len(pal_que) > 0:
            l, h = pal_que.pop()
            #print("pal q", l," ",h)
            nl, nh = self._l_around(s, l, h)
            #print(nh)
            if nh - nl > res[1] - res[0]:
                #print("new res,", nl,":", nh)
                res = nl, nh
            if nl != l or nh != h:
                #print("new pal,", nl,":", nh)
                pal_que.append((nl, nh))
            #print()
        return s[res[0]:res[1]]
