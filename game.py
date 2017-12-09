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
            print("____New game____")
        self.snake = Snake()
        self.number_of_moves = 0
        self.end = False

        coords = {'x': 0, 'y': 0}
        self.snake.tail.add_node(coords)
        self.new_food()
        # self.draw_field()

    def set_strategy(self, number):
        if number == 0:
            self.__strategy = RandomStrategy(self)
        elif number == 1:
            self.__strategy = VectorStrategy(self)
        else:
            self.__strategy = CloserStrategy(self)

    def get_strategy_in_text(self):
        return self.__strategy.name

    def next_move(self):
        selected_dir = self.__strategy.think_and_return_dir()
        # todo: conditions to dir
        self.snake.dir = selected_dir

        self.move_snake_forward()
        self.draw_field()
        if not self.end:
            self.number_of_moves += 1

    def draw_field(self):
        if self.print_game:
            """ Draw whole field in terminal: blank place ., snake tail o, snake head O and food @ """
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
            print('Debug: Snake head: ', self.snake.head['x'], self. snake.head['y'])
            print("Number of nodes: ", self.snake.tail.number_of_nodes)
            print("Number of moves: ", self.number_of_moves)

    def move_snake_forward(self):
        """ Move snake on the field in its Direction """
        head_before_move_coords = Game.copy_coords(self.snake.head)

        self.snake.head = self.field_in_dir(self.snake.head, self.snake.dir)

        # todo: tests
        head_x = self.snake.head['x']
        head_y = self.snake.head['y']

        # Eat food
        if self.is_food(head_x, head_y):
            self.snake.tail.add_node(head_before_move_coords)
            self.new_food()
        # Move tail
        else:
            self.snake.tail.last.coords['x'] = head_before_move_coords['x']
            self.snake.tail.last.coords['y'] = head_before_move_coords['y']
            self.snake.tail.move_tail()
            if self.is_snake_tail(head_x, head_y) or self.is_wall(head_x, head_y):
                self.end = True

    def new_food(self):
        """ Creates new food"""
        rand_x = random.randint(0, self.side - 1)
        rand_y = random.randint(0, self.side - 1)

        # todo: stop cycle when there is nowhere to put food
        while not self.is_empty(rand_x, rand_y):
            rand_x = random.randint(0, self.side - 1)
            rand_y = random.randint(0, self.side - 1)

        if self.food is None:
            self.food = Food(self, {'x': rand_x, 'y': rand_y})
        else:
            self.food.set_coords(rand_x, rand_y)

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
            print("Game over")
            print("Vysledky: ", self.get_strategy_in_text(), " - za ", self.number_of_moves, " kroku posbirala ",
                  self.snake.tail.number_of_nodes, " jidel.")
        return {
            'strategy': self.get_strategy_in_text(),
            'moves': self.number_of_moves,
            'eaten': self.snake.tail.number_of_nodes
        }

# i/o functions:
    @staticmethod
    def copy_coords(coords):
        return {'x': coords['x'], 'y': coords['y']}

    def is_empty(self, x, y):
        """ Return True if snake can move to [x, y]"""
        return not self.is_snake_head(x, y) and not self.is_snake_tail(x, y) and not self.is_wall(x, y) or \
               (self.snake.tail.last.coords['x'] == x and self.snake.tail.last.coords['y'] == y)

    def is_snake_head(self, x, y):
        """ Return True if snake head is on [x, y] """
        return self.snake.head['x'] == x and self.snake.head['y'] == y

    # bad efficiency
    def is_snake_tail(self, x, y):
        """ Return True if snake's tailNode is on [x, y] """
        coords = {'x': x, 'y': y}
        return self.snake.tail.is_node_on_coords(coords)
        # todo: bool list

    def is_food(self, x, y):
        """ Return True if food is on [x, y] """
        return self.food.coords['x'] == x and self.food.coords['y'] == y

    def is_wall(self, x, y):
        """ Return True if [x, y] is out of game field """
        return x < 0 or x > self.side - 1 or y < 0 or y > self.side - 1

    def get_neighbours(self, x, y):
        """ Return list of max 4 dicts that are next to [x, y] (whether or not are empty) """
        result = [{'x': x - 1, 'y': y}, {'x': x + 1, 'y': y}, {'x': x, 'y': y + 1}, {'x': x, 'y': y - 1}]
        for coords in result:
            if self.is_wall(coords['x'], coords['y']):
                result.remove(coords)
        return result

    def is_neighbour(self, center, coord):
        """ Test if two fields are next to each other """
        # todo: test
        for coords in self.get_neighbours(center['x'], center['y']):
            if coords['x'] == coord['x'] and coords['y'] == coord['y']:
                return True
        return False

    #def get_dir_from_head_to_far_field(self, coord):


    def get_dir_from_head_to_neighbour_field(self, coord):
        """ Return direction to [x, y] from snake's head"""

        head_x = self.snake.head['x']
        head_y = self.snake.head['y']
        if not self.is_neighbour(self.snake.head, coord):
            return self.snake.dir

        # todo: cycle
        if coord['x'] == head_x + 1:
            return Direction.RIGHT
        if coord['x'] == head_x - 1:
            return Direction.LEFT
        if coord['y'] == head_y + 1:
            return Direction.DOWN
        return Direction.UP

    def get_available_neighbour_fields(self, x, y):
        # todo: test
        """ Return list of dictionaries (coordinates) that are accessible from x, y by 1 move """
        result = []
        # todo: cycle
        if self.is_empty(x - 1, y):
            result.append({'x': x - 1, 'y': y})
        if self.is_empty(x + 1, y):
            result.append({'x': x + 1, 'y': y})
        if self.is_empty(x, y + 1):
            result.append({'x': x, 'y': y + 1})
        if self.is_empty(x, y - 1):
            result.append({'x': x, 'y': y - 1})
        return result

    @staticmethod
    def field_in_dir(coord, dir):
        """ Return the coordinates that are next to coord in dir direction"""
        result_coords = Game.copy_coords(coord)
        # todo: cycle
        if dir == Direction.RIGHT:
            result_coords['x'] += 1
        elif dir == Direction.LEFT:
            result_coords['x'] -= 1
        elif dir == Direction.UP:
            result_coords['y'] -= 1
        elif dir == Direction.DOWN:
            result_coords['y'] += 1
        return result_coords

    def can_move_there(self, dir):
        """ Return True is snake can move 1 field in direction dir """
        coord = self.field_in_dir(self.snake.head, dir)
        return self.is_empty(coord['x'], coord['y'])
