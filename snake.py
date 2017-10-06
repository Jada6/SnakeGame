from enum import Enum


# should be singleton?
class Snake:
    def __init__(self):
        self.dir = Direction.RIGHT
        self.length = 0
        self.head = {'x': 1, 'y': 0}
        self.tail = Tail(self)


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class TailNode:
    def __init__(self, coords, next=None):
        self.coords = coords
        self.next = next


# singly linked list
class Tail:
    def __init__(self, snake):
        self.snake = snake
        self.first = None
        self.last = None
        self.number_of_nodes = 0

    def move_tail(self):
        self.first.next = self.last
        self.last = self.last.next
        self.first = self.first.next
        self.first.next = None

    def add_node(self, coords):
        self.number_of_nodes += 1
        node = TailNode(coords)
        if self.first is not None:
            self.first.next = node
            self.first = node
        else:
            self.first = node
            self.last = node

    def is_node_on_coords(self, coords):
        """ Returns true, if some node is on coords"""
        temp_node = self.last

        while temp_node is not None:
            if temp_node.coords == coords:
                return True
            temp_node = temp_node.next

        return False

