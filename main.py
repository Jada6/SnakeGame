from game import *
import matplotlib.pyplot as plt


def demo():
    """ Visual demo """
    game = Game(5, True)
    game.game_cycle()


def increasing_field_statistics(repetitions):
    """ Play games, collect data and create a graph.
    After every game, expand the field and play again for repetition times.
    The graph shows average final length of the snake """
    initial_length = 3
    final_length = 30
    result = [[0 for _ in range(final_length-initial_length)] for _ in range(3)]

    # Collect data
    for length in range(initial_length, final_length):
        game = Game(length)
        for _ in range(repetitions):
            for strategy in range(len(Strategy.strategies)):
                game.set_strategy(strategy)
                result[strategy][length-initial_length] \
                    += game.game_cycle()['eaten']

    average = [[x/repetitions for x in strategy] for strategy in result]

    # Draw the graph
    for number, strategy in Strategy.strategies.items():
        plt.plot([i + 3 for i in range(len(result[number]))],
                 [x for x in average[number]], label=strategy)
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
    """ Collect statistics and create graph showing percentage of games
    ended with certain length of the snake on 10x10 field """
    size = 10
    game = Game(size)
    repetition = 100
    result = [[0 for _ in range(repetition)]
              for _ in range(len(Strategy.strategies))]

    # Collect data
    for strategy in range(len(Strategy.strategies)):
        game.set_strategy(strategy)
        for i in range(repetition):
            result[strategy][i] = game.game_cycle()['eaten']

    # Create graph
    bin = [i*5 for i in range(0, 9)]
    plt.hist(([x for x in result[0]],
              [x for x in result[1]],
              [x for x in result[2]]),
             bin,
             alpha=0.8,
             rwidth=0.8,
             label=[strategy for strategy in Strategy.strategies.values()])
    plt.legend()
    plt.suptitle("Snake game statistics")
    plt.title("Percentage of games ended on 10x10 field")
    plt.xlabel("Length of the snake")
    plt.ylabel("Percentage of games")
    plt.savefig("tail.png")


def main():
    """ One demo game and three graphs """
    demo()

    increasing_field_statistics(1)
    increasing_field_statistics(1000)

    tail_distribution()


if __name__ == "__main__":
    main()
