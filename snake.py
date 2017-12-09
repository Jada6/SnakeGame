from enum import Enum


class Snake:
    """ Represents snake """
    def __init__(self):
        self.dir = Direction.RIGHT
        self.head = {'x': 1, 'y': 0}
        self.tail = Tail(self)


class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class TailNode:
    """ Represents node in snake's tail """
    def __init__(self, coords, next=None):
        self.coords = coords
        self.next = next


# singly linked list
# todo: represent with python linked list
class Tail:
    """ Represents tail as a linked list of nodes """
    def __init__(self, snake):
        self.snake = snake
        self.first = None
        self.last = None
        self.number_of_nodes = 0

    def move_tail(self):
        """ Move tail one node forward"""
        self.first.next = self.last
        self.last = self.last.next
        self.first = self.first.next
        self.first.next = None

    def add_node(self, coords):
        """ Add node between head and first node """
        self.number_of_nodes += 1
        node = TailNode(coords)
        if self.first is not None:
            self.first.next = node
            self.first = node
        else:
            self.first = node
            self.last = node

    def is_node_on_coords(self, coords):
        """ Returns true, if some TailNode is on the coords """
        temp_node = self.last

        while temp_node is not None:
            if temp_node.coords == coords:
                return True
            temp_node = temp_node.next

        return False

