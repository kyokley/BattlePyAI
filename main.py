import argparse
from battlePy.series import Series
from battlePy.player import loadPlayerModule


def main():
    parser = argparse.ArgumentParser(description="BattlePyAI")
    parser.add_argument("--p1", action="store", default='samples.random_player',
                        help="module name w agent code for player 1 (eg, samples.random)",
                        metavar="<dir.file>")
    parser.add_argument("--p2", action="store", default='samples.rando_shotdrissian',
                        help="module name w agent code for player 1 (eg, samples.random)",
                        metavar="<dir.file>")
    parser.add_argument("--vis", action="store_true", default=False,
                        help="Turn on game visualization(slow)")
    parser.add_argument("--games", type=int, action="store", default=1000,
                        help="Number of games to play.",
                        metavar="N")
    parser.add_argument("--debug", action="store_true", default=False,
                        help="Enable debug behavior.")
    args = parser.parse_args()

    p1 = loadPlayerModule(args.p1)
    p2 = loadPlayerModule(args.p2)

    series = Series(p1(),
                    p2(),
                    numberOfGames=args.games,
                    showVisualization=args.vis,
                    debug=args.debug,
                    visualizationInterval=.01)
    series.start()

if __name__ == '__main__':
    main()
