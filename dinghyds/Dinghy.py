from battlePy.player import Player
from battlePy.default_config import (BOARD_WIDTH,
                                     BOARD_HEIGHT)
from battlePy.ship import UP, RIGHT
import random


class Dinghy(Player):
    def initPlayer(self, *args, **kwargs):
        self.name = 'Dinghy'

    def newGame(self):
        self.shots = set()
        self.shotTargets = list()
        for i in range(0,10):
          for c in range(0,10):
            if (c % 2) == 0 and (i % 2) == 0:
              shot = (i, c)
            elif (c % 2) == 1 and (i %2) == 1:
              shot = (i, c)
            self.shotTargets.append(shot)
        self.targetSet = set()
        self.shipBumper = list()

    def placeShip():
        pass
    def placeShips(self):
        for ship in self.ships:
          isValid = False
          while not isValid:
            orientation = random.choice([UP, RIGHT])
            location = (random.randint(0, BOARD_WIDTH - 1),
            random.randint(0, BOARD_HEIGHT - 1 - ship.size))
            if orientation == UP:
              ship.placeShip(location, orientation)
              if self.isShipPlacedLegally(ship) and ship not in (self.shipBumper):
                for x in range(0, ship.size-1):
                  shipCheck = (location[0]+x, location[1])
                  if shipCheck not in self.shipBumper:
                    isValid = True
                    for space in range(0,ship.size-1):
                      space1 = (location[0]+1, location[1]+space)
                      self.shipBumper.append(space1)
                      space2 = (location[0], location[1]+space+1)
                      self.shipBumper.append(space2)
                      space3 = (location[0]-1, location[1]+space)
                      self.shipBumper.append(space3)
                      space4 = (location[0], location[1]+space-1)
                      self.shipBumper.append(space4)
            else:
              ship.placeShip(location, orientation)
              if self.isShipPlacedLegally(ship) and ship not in (self.shipBumper):
                for x in range(0, ship.size-1):
                  shipCheck = (location[0]+x, location[1])
                  if shipCheck not in self.shipBumper:
                    isValid = True
                    for space in range(0,ship.size-1):
                      space1 = (location[0]+space+1, location[1])
                      self.shipBumper.append(space1)
                      space2 = (location[0]+space, location[1]+1)
                      self.shipBumper.append(space2)
                      space3 = (location[0]+space-1, location[1])
                      self.shipBumper.append(space3)
                      space4 = (location[0]+space, location[1]-1)

    def fireShot(self):
        if not self.targetSet:
          shot = random.choice(self.shotTargets)
          while shot in self.shots:
            shot = random.choice(self.shotTargets)
        else:
          shot = self.targetSet.pop()
          while shot in self.shots:
            if not self.targetSet:
              while shot in self.shots:
                shot = random.choice(self.shotTargets)
            else:
              shot = self.targetSet.pop()
        self.shots.add(shot)
        if shot in self.shotTargets:
          self.shotTargets.remove(shot)
        return shot 

    def addTargets(self, shot):
        if (shot[0]+1 >= 0) and (shot[0]+1 <= BOARD_WIDTH-1): 
          shot1 = (shot[0]+1, shot[1])
          self.targetSet.add(shot1)
        if (shot[1]+1 >= 0) and (shot[1]+1 <= BOARD_HEIGHT-1): 
          shot2 = (shot[0], shot[1]+1)
          self.targetSet.add(shot2)
        if (shot[0]-1 >= 0) and (shot[0]-1 <= BOARD_WIDTH-1): 
          shot3 = (shot[0]-1, shot[1])
          self.targetSet.add(shot3)
        if (shot[1]-1 >= 0) and (shot[1]-1 <= BOARD_HEIGHT-1): 
          shot4 = (shot[0], shot[1]-1)
          self.targetSet.add(shot4)

    def shotHit(self, shot, shipName):
        self.addTargets(shot)
    def shotMissed(self, shot):
        pass
    def opponentShot(self, shot):
        pass
    def shipSunk(self, shipName):
        pass
    def gameWon(self):
        pass
    def gameLost(self):
        pass
