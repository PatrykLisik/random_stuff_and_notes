# https://leetcode.com/problems/flood-fill/


class Solution:
    def floodFill(
        self, image: list[list[int]], sr: int, sc: int, color: int
    ) -> list[list[int]]:
        visited = set()
        que = []
        que.append((sr, sc))
        target_color = image[sr][sc]

        while len(que) > 0:
            point = que.pop()
            visited.add(point)
            print(point)
            x, y = point
            # left
            if x - 1 >= 0 and image[x - 1][y]==target_color and (x - 1, y) not in visited:
                que.append((x - 1, y))

            # right
            if x + 1 < len(image) and image[x + 1][y]==target_color and (x + 1, y) not in visited:
                que.append((x + 1, y))
            # top
            if y + 1 < len(image[0]) and image[x][y+1]==target_color and (x, y+1) not in visited:
                que.append((x , y+1))
            #bottom
            if y - 1 >= 0 and image[x][y-1]==target_color and (x , y-1) not in visited:
                que.append((x, y-1))
            image[x][y]=color
        return image

