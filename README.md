# BattlePy AI

This repo provides a starting point for developing an AI strategy to run on the BattlePy engine.

In BattlePy, Artificial Intelligence agents are pitted against each other in a computerized form of the classic board game Battleship.

## Battleship Overview

Battleship is a two-player game, played on separate 10x10 boards, where each player places ships on their side of the board, and attempts to find the opponent's ships through placement of shots. The players have no starting knowledge of the placement of the oppenent's ships until they score a hit.

Each player is allowed to make one shot per turn, and is told whether their shit hit or missed a ship. Once a ship has been hit on every coordinate it occupies, it is sunk and the firing player is notified which ship was sunk.

The following ships are alloted to each user:
* Carrier (size 5)
* Battleship (size 4)
* Destroyer (size 3)
* Submarine (size 3)
* Patrol Boat (size 2)

The game is won when all of a player's ships have been sunk.

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

**NOTE:** The code for the game engine may change up until the day of the tournament. Therefore, it is a good idea to git pull this repo and re-run step 3 often to ensure that you are running against the latest code.

## Creating a new AI Agent

### Code Structure
Your agent must live in a python file (.py).

Before you can start implementing the agent, your code should import the Player base class from the battlepy module, and define a subclass of Player:

```python
from battlePy.player import Player

class SinkTheBizMarkee(Player):
    pass

Agent = SinkTheBizMarkee
```

Your class must be assigned to the name Agent in this file for the engine to discover it. 
You may choose to name your player class anything you like as long as you also provide a reference to your actual agent code via the name 'Agent'. 


### A complete Battlepy Agent

But this code isnt enough to play - in fact it will fail since it does not implement the placeShips method properly, and has no implementations for the other methods.

Lets correct that while we look at some of the information available to your agent, and put down placeholders for all the available and required functions that a winning agent should implement..


```python
from battlePy.player import Player

# orientations
from battlePy.ship import UP, DOWN, LEFT, RIGHT
import random

class SinkTheBizMarkee(Player):

    def initPlayer(self, *args, **kwargs):
        """Called once per match, not each game."""
        self.name = 'Super Sink Shipper v3'

    def newGame(self):
        "called once per game"
        pass

    def placeShips(self):
        # must place all ships legally.
        for ship in self.ships: # self.ships is created by the game engine
            if ship.name == "Carrier":
                ship.placeShip((5,5), UP)
            else:
                randx = random.randint(1,10)
                ship.placeShip((randx, 5), UP)

    def fireShot(self):
        """Called once per turn, you must fire"""
        return (0,0) 

    def shotHit(self, shot, shipName):
        """Called when your shot has hit"""
        pass

    def shotMissed(self, shot):
        """Called when your shot has missed"""
        pass

    def opponentShot(self, shot):
        """Called when your opponent shoots"""
        pass

    def shipSunk(self, shipName):
        """Called when you sink a ship."""
        pass

    def gameWon(self):
        """Called when you win."""
        pass

    def gameLost(self):
        """Called when you lose"""
        pass


Agent = SinkTheBizMarkee
```


## Playing Battleship with your Agent

### Game information

The game is played on a 10x10 grid: (0,0) to (9, 9). 
The bottom-left corner of the grid is (0,0):
```
      .......... (9,9)
      ..........
      ..........
      ..........
      ..........
      ..........
      ..........
      ..........
      ..........
(0,0) ..........
```

At the start of the game, you have no information about the other player.


### Game Logic
Every game can be thought of as consisting of 4 phases. Not every phase is required to be implemented but methods are provided to allow flexibility in implementing various AI strategies.


### Pre-Match: Player setup

Your agent class is instantiated once, and persists through the life of the match (multiple games).

The initPlayer function allows you to set up any data you need before the start of the first game.

It is legal and encouraged to retain information within your agent between games - a winning agent may need to employ learning strategies for each opponent.

```python
class SuperAwesomeBattlePyAI(Player):
    ...

    def initPlayer(self, *args, **kwargs):
        ...
```


### Phase 1: Pre-game
Before each actual game begins, the `newGame` method is called. This method may be useful in initializing any variables that need to be set on a per game basis.

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

You may inspect the name and size of the ship to make decision regarding ship placement:
```python
ship.name
ship.size
```


If any ships are placed illegally, the game engine will call the player's `placeShip` method again. Each player has 100 attempts to place all of their ships legally. Failure to do so will result in a forfeit.


Example:
 The agent is placing the battleship(size 4) at (3,3) with orientation UP:

```
      .......... (9,9)
      ..........
      ..........
      ...X......
      ...X......
      ...X......
      ...X<------------(3,3)
      ..........
      ..........
(0,0) ..........
```

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

1. Use any modules available in the python 2.7 standard library, with these exceptions:
 * threading, multiprocessing...
 * pdb, traceback, inspect...
    

2. Any unhandled exceptions will cause the offending AI to lose.

3. Each player has 1 second of computation time per game. Being stuck in a method longer than this will result in a GameClockViolationException being raised.

4. Finally, and most importantly, do not do anything that violates the spirit of the competition. It's easy enough to inspect your opponent's AI instance for the location of all of its ships. But where's the fun in that?

### Testing

'main.py' is the testing program - it will let you specify the agents that should play. 

Here is an example usage that tests a new agent file (newagent.py) over one of the provided samples (samples/random_player.py):


```
python main.py
```

In order to facilitate testing, there is a debug mode. In debug mode, the game clock is disabled and unhandled exceptions will cause execution to halt. Debug mode is turned on by setting the optional --debug argument on the command line when running 'main' or 'tournament' programs.
