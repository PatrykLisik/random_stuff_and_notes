from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


class RandomMover:
    def __init__(self, start: Point, min_moves: int, max_moves: int, catch_radius: float):
        self.start = start
        self.current = start
        self.min_moves = min_moves
        self.max_moves = max_moves
        self.catch_radius = catch_radius
        self.distance = []

    def make_move(self):
        pass

    def compute_distance(self):
        pass

    def stop(self):
        pass
