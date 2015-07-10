# BattlePy AI

This repo provides a starting point for developing an AI strategy to run on the BattlePy engine.

## Getting Started
1. Clone the repo

        git clone https://github.com/kyokley/BattlePyAI.git
        cd BattlePyAI
2. Create a new virtualenv for the game engine

        virtualenv -p python2.7 battlepy
        source battlepy/bin/activate
3. Install the necessary requirements

        pip install --upgrade -r requirements.txt
4. At this point, you should be able to run main. This will run 1000 games of the RandomPlayer versus itself.

        python main.py
*NOTE:* The code for the game engine may change up until the day of the tournament. Therefore, it is a good idea to git pull this repo and re-run step 3 often to ensure that you are running against the latest code.

## Creating a new AI
Every game can be thought of as consisting of 4 phases. Not every phase is required to be implemented but methods are provided to allow flexibility in implementing various AI strategies.

### Phase 1: Pre-game
Before the actual game begins, the `newGame` method is called. This method may be useful in initializing any variables that need to be set on a per game basis.

```python
class SuperAwesomeBattlePyAI(Player):
    ...

    def newGame(self):
        ...
```

### Phase 2: Ship Placement
The `placeShips` method of each AI is called during this phase. Each player AI has access to a list containing all of their ships in the `ships` attribute.

```python
class SuperAwesomeBattlePyAI(Player):
    ...

    def placeShips(self):
        ...
```

Each ship has a `placeShip` method that can be used to put the ship on the board. The `placeShip` method expects a point representing the first ship location and an orientation representing the direction of the ship (You should use the ship orientation enumeration from battlePy.ship).

```python
class Ship(object):
    ...

    def placeShip(self, location, orientation):
        ...
```

If any ships are placed illegally, the game engine will call the player's `placeShip` method again. Each player has 100 attempts to place all of their ships legally. Failure to do so will result in a forfeit.

### Phase 3: Shots Fired
During this phase, players take turns firing shots at their opponent's board. By implementing the `fireShot` method, each player is able to select a cell to fire at. The method is expected to return a 2-tuple representing a horizontal and vertical component. i.e. (x, y).

```python
class SuperAwesomeBattlePyAI(Player):
    ...

    def fireShot(self):
        ...
```

The game engine will allow invalid shots (shots off the board) as well as shots to previously fired upon locations. Shot management is left to the AI.

After firing a shot, various methods are called on both the offensive and defensive players to allow collection of data. For the offensive player, the `shotHit` and `shotMissed` methods are called to reflect whether a ship has been hit or not. The function signatures are as follows:

```python
class SuperAwesomeBattlePyAI(Player):
    ...

    def shotHit(self, shot, shipName):
        ...
    
    def shotMissed(self, shot):
        ...
```

For the defensive player, the `opponentShot` method is called.

```python
class SuperAwesomeBattlePyAI(Player):
    ...

    def opponentShot(self, shot):
        ...
```

When all of a ship's locations have been hit, the ship is sunk. This calls the `shipSunk` method on the offensive player to notify it of which ship has been sunk.

```python
class SuperAwesomeBattlePyAI(Player):
    ...

    def shipSunk(self, shipName):
        ...
```

### Phase 4: End Game
The game is over when all of a player's ships have been sunk. This calls the `gameWon` and `gameLost` methods on the winning and losing players, respectively.

```python
class SuperAwesomeBattlePyAI(Player):
    ...

    def gameWon(self):
        ...

    def gameLost(self):
        ...
```

### Other Rules
In addition to the main rules of the game, there are other conditions that may cause your AI to lose if triggered. 
1. Any unhandled exceptions will cause the offending AI to lose.
2. Each player has 1 second of computation time per game. Being stuck in a method longer than this will result in a GameClockViolationException being raised.

### Testing
In order to facilitate testing, there is a debug mode. In debug mode, the game clock is disabled and unhandled exceptions will cause execution to halt. Debug mode is turned on by setting the optional keyword argument debug to True in the Series or Game classes.
