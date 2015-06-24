from battlePy.tournament import Tournament
from battlePy.random_player import RandomPlayer
from admiral import Admiral

def main():
    tournament = Tournament(RandomPlayer(), Admiral(), 1000)
    tournament.start()
    tournament.printStats()

if __name__ == '__main__':
    main()
