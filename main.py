from battlePy.series import Series
from samples.rando_shotdrissian import RandoShotdrissian
from samples.random_player import RandomPlayer


def main():
    series = Series(
        RandomPlayer(),
        RandoShotdrissian(),
        numberOfGames=1000,
        showVisualization=False,
        visualizationInterval=0.01,
    )
    series.start()


if __name__ == '__main__':
    main()
