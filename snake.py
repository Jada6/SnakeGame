from collections import deque
from enum import Enum


class Snake:
    def __init__(self):
        self.dir = Direction.RIGHT
        self.head = {'x': 1, 'y': 0}
        self.tail = deque([{'x': 0, 'y': 0}])

    def move(self, coords):
        self.tail.popleft()
        self.tail.append(coords)

    def is_node_on_coords(self, coords):
        """ Returns true, if some TailNode is on the coords """
        return coords in self.tail

    def move_head_in_dir(self):
        self.head['x'] += self.dir.value[0]
        self.head['y'] += self.dir.value[1]


class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
