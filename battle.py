import argparse

from battlePy.player import loadPlayerModule
from battlePy.series import Series


def unpackPlayerArg(packedArg):
    """Take a string that may or may not contain multiple space-separated tokens.
    return the first token as the expected player module name, the rest as a single string
    for treatment as args to the instantiated class.
    """
    unpacked = packedArg.split(" ", 1)
    if not unpacked:
        raise ValueError("Unexpected agent arg provided: %s" % packedArg)
    if len(unpacked) == 1:
        # no additional args
        return unpacked[0], None
    else:
        return unpacked[0], unpacked[1]


def main():
    parser = argparse.ArgumentParser(description="BattlePyAI")
    parser.add_argument(
        "--p1",
        action="store",
        default='samples.random_player',
        help="module name of agent for player 1 (eg, samples.random). See code for passing args.",
        metavar="<dir.file>",
    )
    parser.add_argument(
        "--p2",
        action="store",
        default='samples.rando_shotdrissian',
        help="module name w agent code for player 1 (eg, samples.random)",
        metavar="<dir.file>",
    )
    parser.add_argument(
        "--vis",
        action="store_true",
        default=False,
        help="Turn on game visualization(slow)",
    )
    parser.add_argument(
        "--games",
        type=int,
        action="store",
        default=1000,
        help="Number of games to play.",
        metavar="N",
    )
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug behavior."
    )
    args = parser.parse_args()

    p1module, p1arg = unpackPlayerArg(args.p1)
    p2module, p2arg = unpackPlayerArg(args.p2)

    p1 = loadPlayerModule(p1module)
    p2 = loadPlayerModule(p2module)

    # each player is handed an argstring if one was found on the CLI.
    # Thee class can decide what to do with it.
    series = Series(
        p1(argstring=p1arg),
        p2(argstring=p2arg),
        numberOfGames=args.games,
        showVisualization=args.vis,
        debug=args.debug,
        visualizationInterval=0.01,
    )
    series.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
