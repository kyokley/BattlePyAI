# BattlePy AI

This repo provides a starting point for developing an AI strategy to run on the BattlePy engine.

## Getting Started
1. Clone the repo

        ```
        git clone https://github.com/kyokley/BattlePyAI.git
        cd BattlePyAI
        ```
2. Create a new virtualenv for the game engine

        ```
        virtualenv -p python2.7 battlepy
        source battlepy/bin/activate
        ```
3. Install the necessary requirements

        ```
        pip install -r requirements.txt
        ```
4. At this point, you should be able to run main. This will run 1000 games of the RandomPlayer versus itself.

        ```
        python main.py
        ```
## Creating a new AI
Every game is separated into two phases. The first phase is where both players place ships on the board. The second phase is the offensive phase where players take turns shooting at their opponent's board.

### Phase 1: Ship Placement
Ships are placed during the first phase of each game. The placeShips method of each AI is called during this phase. Each player AI has access to a list containing all of their ships in the `ships` attribute.

Each ship has a `placeShip` method that can be used to put the ship on the board. The `placeShip` method expects a point representing the first ship location and an orientation representing the direction of the ship (You should use the ship orientation enumeration from battlePy.ship).

If any ships are placed illegally, the game engine will call the player's `placeShip` method again. Each player has 100 attempts to place all of their ships legally. Failure to do so will result in a forfeit.

### Phase 2: Shots Fired
During this phase, players take turns firing shots at their opponent's board. By implementing the `fireShot` method, each player is able to select a cell to fire at. The method is expected to return a 2-tuple representing a horizontal and vertical component. i.e. (x, y).

The game engine will allow invalid shots (shots off the board) as well as shots to previously fired upon locations. Shot management is left to the AI.

After firing a shot...
