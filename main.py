from battlePy.tournament import Tournament
from random_player import RandomPlayer

def main():
    tournament = Tournament(RandomPlayer(), RandomPlayer(), 1000)
    tournament.start()
    tournament.printStats()

if __name__ == '__main__':
    main()
