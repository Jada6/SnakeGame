import random
from sys import maxsize

from snake import Direction


def count_distance(coord1, coord2):
    return ((coord1['x'] - coord2['x'])**2+(coord1['y'] - coord2['y'])**2)**(1/2)


class Strategy:
    def __init__(self, game):
        self.game = game
        self.name = None

    def think(self):
        """ The strategy logic. Return the next desired direction of the snake. """
        return self.game.snake.dir


class VectorStrategy(Strategy):
    """ Firstly come to the same y, than to the same x"""
    def __init__(self, game):
        super(VectorStrategy, self).__init__(game)
        self.name = "Vector strategy"

    def think(self):
        return self.game.get_dir_from_to(self.game.snake.head, self.game.food.coords)


class CloserStrategy(Strategy):
    """ Come to the closest available neighbour field """
    def __init__(self, game):
        super(CloserStrategy, self).__init__(game)
        self.name = "Closer strategy"

    def think(self):
        coords = self.game.get_available_neighbour_fields(self.game.snake.head)
        max_distance = maxsize
        dir = self.game.snake.dir
        
        for coord in coords:
            distance = count_distance(coord, self.game.food.coords)
            if distance < max_distance:
                max_distance = distance
                dir = self.game.get_dir_from_to(self.game.snake.head, coord)

        return dir


class RandomStrategy(Strategy):
    """ Come to a random neighbour """
    def __init__(self, game):
        super(RandomStrategy, self).__init__(game)
        self.name = "Random strategy"

    def think(self):
        coords = self.game.get_available_neighbour_fields(self.game.snake.head)
        if len(coords) == 0:
            return Direction.UP  # just give up if there is nowhere to move

        random_number = random.randint(0, len(coords)-1)
        coord = coords[random_number]

        return self.game.get_dir_from_to(self.game.snake.head, coord)


class Player(Strategy):
    """ Just for debugging """
    def think(self):
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
