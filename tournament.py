from battlePy.tournament import Tournament
from samples.random_player import RandomPlayer
from samples.rando_shotdrissian import RandoShotdrissian
from admiral.admiral import Admiral
from admiral.admiral2 import Admiral2

def main():
    players = [RandomPlayer,
               RandoShotdrissian,
               Admiral,
               Admiral2,
               ]
    tournament = Tournament(players,
                            numberOfGames=101,
                            debug=False,
                            showVisualization=True,
                            )
    tournament.run()

if __name__ == '__main__':
    main()

