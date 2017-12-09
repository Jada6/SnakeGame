import random
from sys import maxsize

from snake import Direction


def count_distance(coord1, coord2):
    return ((coord1['x'] - coord2['x'])**2+(coord1['y'] - coord2['y'])**2)**(1/2)


class Strategy:
    def __init__(self, game):
        self.game = game
        self.name = None

    def think_and_return_dir(self):
        return self.game.snake.dir


class VectorStrategy(Strategy):
    """ Firstly come to the same y, than to the same x"""
    def __init__(self, game):
        super(VectorStrategy, self).__init__(game)
        self.name = "Vector strategy"

    def think_and_return_dir(self):
        # todo: cycle
        if self.game.food.coords['y'] > self.game.snake.head['y']:
            return Direction.DOWN
        elif self.game.food.coords['y'] < self.game.snake.head['y']:
            return Direction.UP
        elif self.game.food.coords['x'] > self.game.snake.head['x']:
            return Direction.RIGHT
        elif self.game.food.coords['x'] < self.game.snake.head['x']:
            return Direction.LEFT

    # todo: if cant move -> random


class CloserStrategy(Strategy):
    """ Come to the closest available neighbour field """
    def __init__(self, game):
        super(CloserStrategy, self).__init__(game)
        self.name = "Closer strategy"

    def think_and_return_dir(self):
        coords = self.game.get_available_neighbour_fields(self.game.snake.head['x'], self.game.snake.head['y'])

        max_distance = maxsize

        dir = self.game.snake.dir
        
        for coord in coords:
            distance = count_distance(coord, self.game.food.coords)
            if distance < max_distance:
                max_distance = distance
                dir = self.game.get_dir_from_head_to_neighbour_field(coord)

        return dir


class RandomStrategy(Strategy):
    """ Come to a random neighbour """
    def __init__(self, game):
        super(RandomStrategy, self).__init__(game)
        self.name = "Random strategy"

    def think_and_return_dir(self):
        coords = self.game.get_available_neighbour_fields(self.game.snake.head['x'], self.game.snake.head['y'])
        if len(coords) == 0:
            return Direction.UP

        random_number = random.randint(0, len(coords)-1)
        coord = coords[random_number]

        return self.game.get_dir_from_head_to_neighbour_field(coord)


class Player(Strategy):
    """ Just for debugging """
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
