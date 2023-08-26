from battlePy.player import Player
from battlePy.ship import UP, RIGHT
import random

class AdmiralCatbot(Player):
    def initPlayer(self, *args, **kwargs):
        self.name = 'dan'

    def newGame(self):
        self.plannedShots = self.planShots()
        self.previousShots = {} 
        self.hitShips = {'Carrier': [],
                         'Battleship': [],
                         'Submarine': [],
                         'Destroyer': [],
                         'Patrol Boat': []} 

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

    def legalShot(self, shot):
        if shot[0] < 0 or shot[0] > self.currentGame.boardWidth - 1:
            return False
        elif shot[1] < 0 or shot[1] > self.currentGame.boardHeight - 1:
            return False
        elif self.previousShots.get(shot):
            return False
        return True

    def fireShot(self):
        shot = None
        for ship in self.hitShips.keys():
            if len(self.hitShips[ship]) > 0:
                shot = self.destroy(self.hitShips[ship])
        if not shot:
            shot = self.search()
        return shot

    def destroy(self, hits):
        if len(hits) == 1:
            choices = [(hits[0][0]+1, hits[0][1]),
                       (hits[0][0]-1, hits[0][1]),
                       (hits[0][0], hits[0][1]+1),
                       (hits[0][0], hits[0][1]-1)]
            shot = random.choice(choices)
            while not self.legalShot(shot):
                choices.remove(shot)
                shot = random.choice(choices)
        elif hits[0][0] == hits[1][0]: #vertical
            choices = [(min(hits)[0], min(hits)[1]-1),
                       (max(hits)[0], max(hits)[1]+1)]
            shot = random.choice(choices)
            if not self.legalShot(shot):
                choices.remove(shot)
            shot = choices[0]
        else: #horizontal
            choices = [(min(hits)[0]-1, min(hits)[1]),
                       (max(hits)[0]+1, max(hits)[1])]
            shot = random.choice(choices)
            if not self.legalShot(shot):
                choices.remove(shot)
            shot = choices[0]
        return shot

    def search(self):
        remaining = list(set(self.plannedShots).difference(self.previousShots.keys()))
        return random.choice(remaining)

    def shotHit(self, shot, shipName):
        self.previousShots[shot] = shipName
        self.hitShips[shipName].append(shot)

    def shotMissed(self, shot):
        self.previousShots[shot] = 'miss'

    def shipSunk(self, shipName):
        self.hitShips.pop(shipName)

    def planShots(self):
        shots = [] 
        for x in range(0, 10):
            if x % 2:
                for y in range(0,10, 2):
                    shots.append((x,y)) 
            else:
                for y in range(1,10, 2):
                    shots.append((x,y))
        return shots

Agent = AdmiralCatbot 
