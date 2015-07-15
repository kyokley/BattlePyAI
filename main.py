import argparse
from importlib import import_module
from battlePy.series import Series


# TODO: move me to the engine?
def loadPlayer(module_path):
    """Import the function "planner" from the specific planner module file and return it."""
    agentModule = import_module(module_path)
    return agentModule.Agent()


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

    p1 = loadPlayer(args.p1)
    p2 = loadPlayer(args.p2)

    series = Series(p1,
                    p2,
                    numberOfGames=args.games,
                    showVisualization=args.vis,
                    debug=args.debug,
                    visualizationInterval=.01)
    series.start()

if __name__ == '__main__':
    main()
