import time, random

from snake import Snake, Direction
from strategies import *
from food import Food


class Game:
    def __init__(self):
        self.side = 10
        self.snake = Snake()
        self.strategy = CloserStrategy(self)
        self.end = False
        self.number_of_moves = 0

        food_coords = {'x': 3, 'y': 3}
        self.food = Food(food_coords)
        '''
        coords = {'x': 0, 'y': 3}
        self.snake.tail.add_node(coords)
        print(self.snake.tail.is_node_on_coords(coords))

        coords = {'x': 0, 'y': 2}
        self.snake.tail.add_node(coords)
        print(self.snake.tail.is_node_on_coords(coords))

        coords = {'x': 0, 'y': 1}
        self.snake.tail.add_node(coords)
        print(self.snake.tail.is_node_on_coords(coords))
        '''
        coords = {'x': 0, 'y': 0}
        self.snake.tail.add_node(coords)
        print(self.snake.tail.is_node_on_coords(coords))

        self.draw_field()
        self.game_cycle()

    def next_move(self):
        selected_dir = self.strategy.think_and_return_dir()
        # todo: conditions to dir
        self.snake.dir = selected_dir

        self.move_snake_forward()
        self.draw_field()
        self.number_of_moves += 1
        print("Number of moves: ", self.number_of_moves)

    def draw_field(self):
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

    def move_snake_forward(self):
        head_before_move_coords = {'x': self.snake.head['x'], 'y': self.snake.head['y']}

        """ Move snake on the field in its Direction """
        if self.snake.dir == Direction.RIGHT:
            self.snake.head['x'] += 1
        elif self.snake.dir == Direction.LEFT:
            self.snake.head['x'] -= 1
        elif self.snake.dir == Direction.UP:
            self.snake.head['y'] -= 1
        elif self.snake.dir == Direction.DOWN:
            self.snake.head['y'] += 1

        # todo: tests
        head_x = self.snake.head['x']
        head_y = self.snake.head['y']

        if self.is_food(head_x, head_y):
            self.snake.tail.add_node(head_before_move_coords)
            self.new_food()
        else:
            self.snake.tail.last.coords['x'] = head_before_move_coords['x']
            self.snake.tail.last.coords['y'] = head_before_move_coords['y']
            self.snake.tail.move_tail()
            if self.is_snake_tail(head_x, head_y) or self.is_wall(head_x, head_y):
                print("Game over")
                self.end = True

    def new_food(self):
        rand_x = random.randint(0, self.side - 1)
        rand_y = random.randint(0, self.side - 1)

        while not self.is_empty(rand_x, rand_y):
            rand_x = random.randint(0, self.side - 1)
            rand_y = random.randint(0, self.side - 1)

        # todo: food setter
        self.food.coords['x'] = rand_x
        self.food.coords['y'] = rand_y
        self.draw_field()

    def game_cycle(self):
        """ The main game loop """
        while not self.end:
            self.next_move()
            time.sleep(0.01)

    # todo: end_game

# i/o functions:
    # todo: copy coords

    # very, very bad efficiency
    def is_empty(self, x, y):
        return not self.is_snake_head(x, y) and not self.is_snake_tail(x, y) and not self.is_wall(x, y)

    def is_snake_head(self, x, y):
        return self.snake.head['x'] == x and self.snake.head['y'] == y

    # bad efficiency
    def is_snake_tail(self, x, y):
        coords = {'x': x, 'y': y}
        return self.snake.tail.is_node_on_coords(coords)
        # todo: bool list

    def is_food(self, x, y):
        return self.food.coords['x'] == x and self.food.coords['y'] == y

    def is_wall(self, x, y):
        return x < 0 or x > self.side - 1 or y < 0 or y > self.side - 1

    def get_neighbours(self, x, y):
        """ Return list of 4 dicts that are next to [x, y] (whether or not are empty) """
        result = [{'x': x - 1, 'y': y}, {'x': x + 1, 'y': y}, {'x': x, 'y': y + 1}, {'x': x, 'y': y - 1}]
        for coords in result:
            if self.is_wall(coords['x'], coords['y']):
                result.remove(coords)
        return result

    def is_neighbour(self, center_x, center_y, x, y):
        """ Test if two fields are next to each other """
        # todo: test
        for coords in self.get_neighbours(center_x, center_y):
            if coords['x'] == x and coords['y'] == y:
                return True
        return False

    def get_dir_from_head_to_field(self, coord):
        """ Return direction to [x, y] from snake's head"""

        head_x = self.snake.head['x']
        head_y = self.snake.head['y']
        if not self.is_neighbour(self.snake.head['x'], self.snake.head['y'], coord['x'], coord['y']):
            return self.snake.dir

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
        if self.is_empty(x - 1, y):
            result.append({'x': x - 1, 'y': y})
        if self.is_empty(x + 1, y):
            result.append({'x': x + 1, 'y': y})
        if self.is_empty(x, y + 1):
            result.append({'x': x, 'y': y + 1})
        if self.is_empty(x, y - 1):
            result.append({'x': x, 'y': y - 1})
        return result


game = Game()
