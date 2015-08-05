from battlePy.player import Player

# orientations
from battlePy.ship import UP, DOWN, LEFT, RIGHT
import random
from copy import copy


class CommanderBernum(Player):

    def initPlayer(self, *args, **kwargs):
        """Called once per match, not each game."""
        self.name = 'Commander Bernum'

    def newGame(self):
        "called once per game"
        self.hitShips = {}
        for ship in self.ships:
            self.hitShips[ship.name] = []

        # Start out board shots. Will remove as we shoot.
        self.validShots = [(x, y) for x in range(10) for y in range(10)]
        self.destroyedShips = []  # what ships are destroyed this round
        self.finishHim = False

    def placeShips(self):
        # must place all ships legally.for ship in self.ships:
        for ship in self.ships:
            isValid = False
            while not isValid:
                orientation = random.choice([UP, RIGHT])
                if orientation == UP:
                    location = (random.randint(0, self.currentGame.boardWidth - 1),
                                random.randint(0, self.currentGame.boardHeight - 1 - ship.size))
                else:
                    location = (random.randint(0, self.currentGame.boardWidth - 1 - ship.size),
                                random.randint(0, self.currentGame.boardHeight - 1))
                ship.placeShip(location, orientation)

                if self.isShipPlacedLegally(ship):
                    isValid = True

    def fireShot(self):
        """Called once per turn, you must fire"""
        height = self.currentGame.boardWidth - 1
        width = self.currentGame.boardHeight - 1

        takenShot = None
        validShot = False
        while not validShot:
            if self.finishHim == True:
                takenShot = self.chooseShot()

            if takenShot is None:
                takenShot = random.choice(self.validShots)

            if takenShot in self.validShots:  # Only take shots we haven't taken yet
                validShot = True

        self.validShots.remove(takenShot)

        return takenShot

    def chooseShot(self):
        # Shoot in one of the next four directions if we're trying to
        # finish off the ship
        nextShots = [(self.previousShot[0] + 1, self.previousShot[1]), # right
                     (self.previousShot[0] - 1, self.previousShot[1]), # left
                     (self.previousShot[0], self.previousShot[1] - 1), # down
                     (self.previousShot[0], self.previousShot[1] + 1)] # up
        validNextShots = copy(nextShots)
        for shot in nextShots:
            # Check if any of the next up/down/left/right shots are
            # valid ones we haven't done yet.
            if shot not in self.validShots:
                validNextShots.remove(shot)

        if len(validNextShots) > 0:
            # So long as there's been one valid shot, take one of them
            takenShot = random.choice(nextShots)
        else:
            # We've reached the end of the ship. If we haven't sunk it
            # then we should turn around. Logic not implemented for
            # that yet so just reset everything and hope we finish
            # it off via random shots.
            takenShot = None
            self.resetNextShotLogic()

        return takenShot

    def resetNextShotLogic(self):
        # Reset next shot logic when we've either finished off a ship or
        # we might get stuck trying to figure out next shot.
        self.finishHim = False
        self.previousShot = None

        # implement directional choice logic at some point
        self.directions = ['horizontal', 'vertical']
        self.directionToFire = random.choice(self.directions)

    def shotHit(self, shot, shipName):
        """Called when your shot has hit"""
        self.hitShips[shipName].append(shot)
        ship = [x for x in self.ships if x.name == shipName][0]
        if ship.isSunk():
            self.destroyedShips.append(shipName)
            self.resetNextShotLogic()
        else:
            self.previousShot = shot
            self.finishHim = True

    def shotMissed(self, shot):
        """Called when your shot has missed"""
        #if self.finishHim == True:  # Missed while trying to finish a ship off
        #    # Remove the direction you were firing and choose a new one
        #    self.directions.remove(self.directionToFire)
        #    self.directionToFire = random.choice(self.directions)

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


Agent = CommanderBernum
