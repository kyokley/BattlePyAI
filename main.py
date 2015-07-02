from battlePy.series import Series
from random_player import RandomPlayer

def main():
    series = Series(RandomPlayer(), RandomPlayer(), 1000)
    series.start()
    series.printStats()

if __name__ == '__main__':
    main()
