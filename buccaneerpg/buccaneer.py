from battlePy.player import Player
from battlePy.ship import UP, RIGHT, DOWN, LEFT
import random
import time



class Buccaneer(Player):
    stats = []
    def newGame(self):
        self.hittingShip = False
        self.findingDirectionOfShip = False
        self.hitList = []
        self.huntList = []
        self.modifier = (0,0)
        self.origin = (0,0)
        self.curShip = ''
        self.accidentalHits = []
        self.accidentalShip = ''
        self.shotsFired = 0
        for row in range(10):
            for col in range(10):
                if(self.isChecker((col,row,), 2)):
                    self.hitList.append((col,row))
        random.shuffle(self.hitList)

    def isChecker(self, coor, parity):
        return coor[0]%parity == coor[1]%parity

    def placeShips(self):
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
        #Normal Case
        self.shotsFired += 1   
        if self.hittingShip == False and self.hitList:
            nextShot = self.hitList.pop()
            if nextShot in self.accidentalHits:
                self.shotHit(nextShot, self.accidentalShip)
                self.shotsFired -= 1
                return self.fireShot()
            return nextShot
        elif self.huntList:
            self.modifier = self.huntList.pop()
            #import pdb; pdb.set_trace()
            target = tuple(x+y for x,y in zip(self.origin, self.modifier))
            try:
                self.hitList.remove(target)
            except:
                pass
            return target
        else:
            self.hittingShip = False
        return(0,0)
       
    def shotHit(self, shot, shipName):
        
        if self.hittingShip == False:
            self.huntList = []
            self.huntList.append((1, 0))
            self.huntList.append((-1, 0))
            self.huntList.append((0, 1))
            self.huntList.append((0,-1))
            self.origin = shot
            self.curShip = shipName
            self.hittingShip = True
        
        elif self.curShip == shipName:
            
            if self.modifier[0] > 0:
                self.huntList.append((self.modifier[0]+1, self.modifier[1]))
            elif self.modifier[0] < 0:
                self.huntList.append((self.modifier[0]-1, self.modifier[1]))
            elif self.modifier[1] > 0:
                self.huntList.append((self.modifier[0], self.modifier[1]+1))
            elif self.modifier[1] < 0:
                self.huntList.append((self.modifier[0], self.modifier[1]-1))

        else:
            self.accidentalHits.append(shot)
            self.hitList.append(shot)
            self.accidentalShip = shipName


    def shipSunk(self, shipName):
        self.hittingShip = False

    def gameWon(self):
        self.stats.append(self.shotsFired)
    
    def gameLost(self):
        self.stats.append(self.shotsFired)
        time.sleep(2)
        #import pdb; pdb.set_trace()
    
    def getStats(self):
        return self.stats        
