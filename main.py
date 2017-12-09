from game import *
import matplotlib.pyplot as plt

game = Game(5, True)
game.game_cycle()

result1 = []
result2 = []
result3 = []

for i in range(3, 30):
    game = Game(i)
    game.set_strategy(2)
    result1.append(game.game_cycle())

    game.set_strategy(0)
    result2.append(game.game_cycle())

    game.set_strategy(1)
    result3.append(game.game_cycle())

'''
result1.sort(key=lambda x: x['eaten'], reverse=True)
result2.sort(key=lambda x: x['eaten'], reverse=True)
result3.sort(key=lambda x: x['eaten'], reverse=True)
'''
i = 0
x = []
y = []
print([i['eaten'] for i in result1])
print([i['eaten'] for i in result2])
print([i['eaten'] for i in result3])


plt.plot([i + 3 for i in range(len(result1))], [x['eaten'] for x in result1], label='Closer strategy')
plt.plot([i + 3 for i in range(len(result2))], [x['eaten'] for x in result2], label='Random strategy')
plt.plot([i + 3 for i in range(len(result3))], [x['eaten'] for x in result3], label='Vector strategy')
plt.legend()
'''
bin = [i*5 for i in range(1, 10)]
plt.hist([x['eaten'] for x in result1], bin, rwidth=0.5, color='b')
plt.hist([x['eaten'] for x in result2], bin, rwidth=0.5, color='g')
plt.hist([x['eaten'] for x in result3], bin, rwidth=0.5, color='y')
'''
'''
for strategy in result1:
    print(strategy['strategy'], strategy['eaten'])
    x.append(i)
    y.append(strategy['eaten'])
    i += 1
'''

# plt.plot(x, y)
plt.ylabel('Length of snake')
plt.title('Snake Game statistics')
plt.savefig("test.png")
