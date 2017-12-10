import time

from snake import Snake
from strategies import *
from food import Food


class Game:
    def __init__(self, n=10, print_game=False):
        self.side = n
        self.snake = None
        self.__strategy = CloserStrategy(self)
        self.end = False
        self.number_of_moves = None
        self.food = None
        self.print_game = print_game

    def prepare_game(self):
        if self.print_game:
            print("\n____New game____")
        self.snake = Snake()
        self.number_of_moves = 0
        self.end = False
        self.new_food()
        self.draw_field()

    def set_strategy(self, number):
        if number == 0:
            self.__strategy = RandomStrategy(self)
        elif number == 1:
            self.__strategy = VectorStrategy(self)
        else:
            self.__strategy = CloserStrategy(self)

    def next_move(self):
        self.snake.dir = self.__strategy.think()
        self.move_snake_forward()
        self.draw_field()
        if not self.end:
            self.number_of_moves += 1

    def draw_field(self):
        """ If the printing is set, draw whole field in console:
        blank place ., wall #, snake tail o, snake head O and food @ """
        if self.print_game:
            for y in range(-1, self.side+1):
                for x in range(-1, self.side+1):
                    if self.is_snake_head(x, y):
                        print('O', end=' ')  # head
                    elif self.is_snake_tail(x, y):
                        print('o', end=' ')  # tail node
                    elif self.is_food(x, y):
                        print('@', end=' ')  # food
                    elif self.is_wall(x, y):
                        print('#', end=' ')  # wall
                    else:
                        print('.', end=' ')  # nothing
                print()
            #print('Debug: Snake head: ', self.snake.head['x'], self. snake.head['y'])
            print("Length of the tail:", len(self.snake.tail))
            print("Number of moves:", self.number_of_moves)

    def move_snake_forward(self):
        """ Move snake on the field in its Direction """
        snake = self.snake
        head_before_move_coords = self.copy_coords(snake.head)

        snake.move_head_in_dir()
        head = snake.head

        # Eat food
        if self.is_food(head['x'], head['y']):
            snake.tail.append(head_before_move_coords)
            self.new_food()
        # Move tail
        else:
            snake.move(head_before_move_coords)

            #snake.tail.last.coords = head_before_move_coords
            #snake.tail.move_tail()
            if self.is_snake_tail(head['x'], head['y']) or self.is_wall(head['x'], head['y']):
                self.end = True

    def new_food(self):
        """ Creates new food """
        coord = self.random_coord()
        while not self.is_empty(coord[0], coord[1]):
            coord = self.random_coord()

        if self.food is None:
            self.food = Food(self, {'x': coord[0], 'y': coord[1]})
        else:
            self.food.set_coords(coord[0], coord[1])

    def game_cycle(self):
        """ The main game loop """
        self.prepare_game()

        while not self.end:
            self.next_move()
            if self.print_game:
                time.sleep(0.25)
        return self.end_game()

    def end_game(self):
        """ The output after the game is over """
        if self.print_game:
            print("\n_____ Game over _____")
            print(self.get_strategy_in_text(), "collected", len(self.snake.tail),
                  "food after", self.number_of_moves, "moves.")
        return {
            'strategy': self.get_strategy_in_text(),
            'moves': self.number_of_moves,
            'eaten': len(self.snake.tail)
        }

# i/o functions:
    def get_strategy_in_text(self):
        return self.__strategy.name

    def copy_coords(self, coords):
        return {'x': coords['x'], 'y': coords['y']}

    def is_empty(self, x, y):
        """ Return True if snake can move to [x, y]"""
        return not self.is_snake_head(x, y) and not self.is_snake_tail(x, y) and not self.is_wall(x, y) or \
            (self.snake.tail[0]['x'] == x and self.snake.tail[0]['y'] == y)

    def is_snake_head(self, x, y):
        return self.snake.head['x'] == x and self.snake.head['y'] == y

    def is_snake_tail(self, x, y):
        coords = {'x': x, 'y': y}
        return self.snake.is_node_on_coords(coords)

    def is_food(self, x, y):
        return self.food.coords['x'] == x and self.food.coords['y'] == y

    def is_wall(self, x, y):
        """ Return True if [x, y] is out of game field """
        return x < 0 or x > self.side - 1 or y < 0 or y > self.side - 1

    def get_dir_from_to(self, from_coord, where_coord):
        vectors = [direction.value for direction in Direction]

        i = 0
        for dir in ['x', 'y']:
            for vector in vectors[i:2+i]:
                if (where_coord[dir] - from_coord[dir]) * vector[i//2] > 0:
                    return Direction(vector)
            i += 2
        """
        if where_coord['y'] > from_coord['y']:
            return Direction.DOWN
        elif where_coord['y'] < from_coord['y']:
            return Direction.UP
        elif where_coord['x'] > from_coord['x']:
            return Direction.RIGHT
        elif where_coord['x'] < from_coord['x']:
            return Direction.LEFT
        """
        return self.snake.dir

    def get_available_neighbour_fields(self, coords):
        """ Return list of dictionaries (coordinates) that are accessible from x, y by 1 move """
        x = coords['x']
        y = coords['y']
        result = []
        vectors = [direction.value for direction in Direction]
        for vector in vectors:
            new_x = x + vector[0]
            new_y = y + vector[1]
            if self.is_empty(new_x, new_y):
                result.append({'x': new_x, 'y': new_y})
        return result

    def random_coord(self):
        coord = [0, 0]
        for i in range(2):
            coord[i] = random.randint(0, self.side - 1)
        return coord
    '''
    def can_move_there(self, dir):
        """ Return True is snake can move 1 field in direction dir """
        coord = self.field_in_dir(self.snake.head, dir)
        return self.is_empty(coord['x'], coord['y'])
    '''