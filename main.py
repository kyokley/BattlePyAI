from battlePy.series import Series
from samples.random_player import RandomPlayer
from samples.rando_shotdrissian import RandoShotdrissian

def main():
    series = Series(RandomPlayer(),
                    RandoShotdrissian(),
                    numberOfGames=1000,
                    showVisualization=False,
                    visualizationInterval=.01)
    series.start()

if __name__ == '__main__':
    main()
