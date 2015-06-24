from player import Player
from config import (BOARD_WIDTH,
                    BOARD_HEIGHT)
from ship import UP, RIGHT
import random

class RandomPlayer(Player):
    def initPlayer(self):
        self.name = 'RandomPlayer'

    def placeShips(self):
        for ship in self.ships:
            isValid = False
            while not isValid:
                orientation = random.choice([UP, RIGHT])
                if orientation == UP:
                    location = (random.randint(0, BOARD_WIDTH - 1),
                                random.randint(0, BOARD_HEIGHT - 1 - ship.size))
                else:
                    location = (random.randint(0, BOARD_WIDTH - 1 - ship.size),
                                random.randint(0, BOARD_HEIGHT - 1))
                ship.placeShip(location, orientation)

                if self.isShipPlacedLegally(ship):
                    isValid = True

    def fireShot(self):
        return (random.randint(0, BOARD_WIDTH - 1),
                random.randint(0, BOARD_HEIGHT - 1))
