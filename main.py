from game import *
import matplotlib.pyplot as plt


# Demo of Snake
def demo():
    game = Game(10, True)
    game.set_strategy(1)
    game.game_cycle()


def increasing_field_statistics(repetitions):
    initial_length = 3
    final_length = 30
    result = [[0 for _ in range(final_length-initial_length)] for _ in range(3)]

    # Collect data
    for length in range(initial_length, final_length):
        game = Game(length)
        for _ in range(repetitions):
            for strategy in range(3):
                game.set_strategy(strategy)
                result[strategy][length-initial_length] += game.game_cycle()['eaten']

    average = [[x/repetitions for x in strategy] for strategy in result]

    plt.plot([i + 3 for i in range(len(result[0]))], [x for x in average[0]], label='Random strategy')
    plt.plot([i + 3 for i in range(len(result[1]))], [x for x in average[1]], label='Vector strategy')
    plt.plot([i + 3 for i in range(len(result[2]))], [x for x in average[2]], label='Closer strategy')
    plt.legend()

    plt.suptitle('Snake game statistics')
    title = "Final " if repetitions == 1 else "Average final "
    title += "length of the snake after " + str(repetitions)
    title += " game" if repetitions == 1 else " games"
    plt.title(title)
    plt.ylabel('Final length of snake')
    plt.xlabel('Size of the field')
    plt.savefig("increasing_field_" + str(repetitions) + ".png")

    # Clear the plot
    plt.clf()
    plt.cla()
    plt.close()


def tail_distribution():
    """ Collect statistics and create graph showing
    percentage of games ended with certain length of the snake on 10x10 field """
    size = 10
    game = Game(size)
    repetition = 100
    result = [[0 for _ in range(repetition)] for _ in range(3)]

    # Collect data
    for strategy in range(3):
        game.set_strategy(strategy)
        for i in range(repetition):
            result[strategy][i] = game.game_cycle()['eaten']

    bin = [i*5 for i in range(0, 9)]
    plt.hist(([x for x in result[0]], [x for x in result[1]], [x for x in result[2]]),
             bin,
             alpha=0.8,
             rwidth=0.8,
             label=["RandomStrategy", "VectorStrategy", "CloserStrategy"])
    plt.legend()
    plt.suptitle("Snake game statistics")
    plt.title("Percentage of games ended on 10x10 field")
    plt.xlabel("Length of the snake")
    plt.ylabel("Percentage of games")
    plt.savefig("tail.png")


#demo()

#increasing_field_statistics(1)
increasing_field_statistics(1000)

#tail_distribution()
