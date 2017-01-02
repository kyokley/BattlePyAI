import argparse
from battlePy.tournament import Tournament
from battlePy.player import loadPlayerModule

def main():
    demo_roster = [
            "samples.rando_shotdrissian",
            "samples.random_player",
            ]

    parser = argparse.ArgumentParser(description="BattlePyAI Tournament")
    parser.add_argument('players', metavar='<dir.file>', type=str,
                        nargs="*",
                        help="module name w agent code for player (eg, samples.random)"
                        )
    parser.add_argument("--vis", action="store_true", default=False,
                        help="Turn on game visualization(slow)")
    parser.add_argument("--games", type=int, action="store", default=101,
                        help="Number of games to play.",
                        metavar="N")
    parser.add_argument("--debug", action="store_true", default=False,
                        help="Enable debug behavior.")
    args = parser.parse_args()


    if not args.players:
        agent_modules = demo_roster
    else:
        agent_modules = args.players

    players = []
    for agent_module in agent_modules:
        players.append(loadPlayerModule(agent_module))

    tournament = Tournament(players,
                            numberOfGames=args.games,
                            debug=args.debug,
                            showVisualization=args.vis,
                            )
    tournament.run()

if __name__ == '__main__':
    main()

