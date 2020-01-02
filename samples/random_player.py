import random

from battlePy.player import Player
from battlePy.ship import RIGHT, UP


class RandomPlayer(Player):
    def placeShips(self):
        for ship in self.ships:
            isValid = False
            while not isValid:
                orientation = random.choice([UP, RIGHT])
                if orientation == UP:
                    location = (
                        random.randint(0, self.currentGame.boardWidth - 1),
                        random.randint(0, self.currentGame.boardHeight - 1 - ship.size),
                    )
                else:
                    location = (
                        random.randint(0, self.currentGame.boardWidth - 1 - ship.size),
                        random.randint(0, self.currentGame.boardHeight - 1),
                    )
                ship.placeShip(location, orientation)

                if self.isShipPlacedLegally(ship):
                    isValid = True

    def fireShot(self):
        return (
            random.randint(0, self.currentGame.boardWidth - 1),
            random.randint(0, self.currentGame.boardHeight - 1),
        )


Agent = RandomPlayer
