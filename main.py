from game import *

result = []

for i in range(200):
    game = Game(10)
    game.set_strategy(2)
    result.append(game.game_cycle())

    game.set_strategy(0)
    result.append(game.game_cycle())

    game.set_strategy(1)
    result.append(game.game_cycle())

result.sort(key=lambda x: x['eaten'], reverse=True)

for strategy in result:
    print(strategy['strategy'], strategy['eaten'])
