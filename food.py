class Food:
    def __init__(self, game, coords):
        self.game = game
        self.coords = coords

    def set_coords(self, x, y):
        self.coords['x'] = x
        self.coords['y'] = y
        self.game.draw_field()
