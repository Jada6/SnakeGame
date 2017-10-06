import random

from snake import Direction


# todo: superclass

class ForwardStrategy:
    def __init__(self, game):
        self.game = game

    def think_and_return_dir(self):
        return self.game.snake.dir


class VectorStrategy:
    def __init__(self, game):
        self.game = game

    def think_and_return_dir(self):
        if self.game.food.coords['y'] > self.game.snake.head['y']:
            return Direction.DOWN
        elif self.game.food.coords['y'] < self.game.snake.head['y']:
            return Direction.UP
        elif self.game.food.coords['x'] > self.game.snake.head['x']:
            return Direction.RIGHT
        elif self.game.food.coords['x'] < self.game.snake.head['x']:
            return Direction.LEFT


class ClosestStrategy:
    def __init__(self, game):
        self.game = game

    def think_and_return_dir(self):
        coords = self.game.get_available_neighbour_fields(self.game.snake.head['x'], self.game.snake.head['y'])

        for coord in coords:
            self.count_distance(coord, self.game.food.coords)

    def count_distance(self, coord1, coord2):
        return ((coord1['x'] - coord2['x'])**2+(coord1['y'] - coord2['y'])**2)**(1/2)


class RandomStrategy:
    def __init__(self, game):
        self.game = game

    def think_and_return_dir(self):
        coords = self.game.get_available_neighbour_fields(self.game.snake.head['x'], self.game.snake.head['y'])
        if len(coords) == 0:
            return Direction.UP

        random_number = random.randint(0, len(coords)-1)
        coord = coords[random_number]

        if coord[1] > self.game.snake.head['y']:
            return Direction.DOWN
        elif coord[1] < self.game.snake.head['y']:
            return Direction.UP
        elif coord[0] > self.game.snake.head['x']:
            return Direction.RIGHT
        elif coord[0] < self.game.snake.head['x']:
            return Direction.LEFT
        return self.game.snake.dir


class Player:
    def __init__(self, game):
        self.game = game

    def think_and_return_dir(self):
        key = input()
        if key == 'w':
            return Direction.UP
        if key == 'd':
            return Direction.RIGHT
        if key == 's':
            return Direction.DOWN
        if key == 'a':
            return Direction.LEFT
        return self.game.snake.dir
