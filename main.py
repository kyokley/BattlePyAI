from battlePy.series import Series
from random_player import RandomPlayer

def main():
    series = Series(RandomPlayer(),
                    RandomPlayer(),
                    numberOfGames=1000,
                    showVisualization=False,
                    visualizationInterval=.01)
    series.start()

if __name__ == '__main__':
    main()
