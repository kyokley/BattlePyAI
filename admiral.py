from battlePy.player import Player
from config import (BOARD_WIDTH,
                    BOARD_HEIGHT,
                    DEFAULT_SHIPS)
from battlePy.ship import (UP,
                           RIGHT,
                           LEFT,
                           DOWN,
                           SHIP_ORIENTATIONS,
                           VECTOR_DICT,
                           )
import random, math

VERSION = 'v0.1'
(SEARCH,
 DESTROY,
 RANDOM) = OFFENSIVE_MODES = range(3)

def intToPoint(num):
    x = num % BOARD_WIDTH
    y = num / BOARD_WIDTH
    return x, y

def pointToInt(point):
    total = point[0] + BOARD_WIDTH * point[1]
    return total

def isValidPoint(point):
    return (0 <= point[0] < BOARD_WIDTH and
            0 <= point[1] < BOARD_HEIGHT)

def findMinMaxPoint(points):
    minPoint = None
    maxPoint = None
    for point in points:
        if not maxPoint:
            maxPoint = point
        if not minPoint:
            minPoint = point
        maxDist = getDistance(maxPoint[0], maxPoint[1])
        minDist = getDistance(minPoint[0], minPoint[1])
        pointDist = getDistance(point[0], point[1])

        if pointDist > maxDist:
            maxPoint = point
        if pointDist < minDist:
            minPoint = point
    return minPoint, maxPoint

def normalize(shot):
    if shot[0] > 0:
        x = 1
    elif shot[0] < 0:
        x = -1
    else:
        x = 0

    if shot[1] > 0:
        y = 1
    elif shot[1] < 0:
        y = -1
    else:
        y = 0

    return x, y

def getDistance(x, y):
    dist = math.sqrt(x**2 + y**2)
    return dist

class Admiral(Player):
    def initPlayer(self):
        self.name = 'Admiral %s' % VERSION
        self.shipSizes = dict(((x[0], x[1]) for x in DEFAULT_SHIPS))

    def newGame(self):
        self.shots = set()
        self.foundShips = dict(((x[0], []) for x in DEFAULT_SHIPS))
        self.searchMat = []
        self.killMats = dict(((x[0], set()) for x in DEFAULT_SHIPS))

        self.offense = SEARCH

        for i in xrange(BOARD_HEIGHT):
            for j in xrange(i % 2, BOARD_WIDTH, 2):
                self.searchMat.append((i, j))

    def shotHit(self, shot, shipName):
        hitLocations = self.foundShips[shipName]
        hitLocations.append(shot)

        if len(hitLocations) > 1:
            # Filter out impossible locations
            minPoint, maxPoint = findMinMaxPoint(hitLocations)

            shipLine = normalize((maxPoint[0] - minPoint[0],
                                       maxPoint[1] - minPoint[1]))

            possibleLocations = []
            for i in xrange(1, self.shipSizes[shipName]):
                possibleShot = (minPoint[0] - i * shipLine[0],
                                minPoint[1] - i * shipLine[1])
                if isValidPoint(possibleShot):
                    possibleLocations.append(possibleShot)

                possibleShot = (minPoint[0] + i * shipLine[0],
                                minPoint[1] + i * shipLine[1])
                if isValidPoint(possibleShot):
                    possibleLocations.append(possibleShot)

                possibleShot = (maxPoint[0] + i * shipLine[0],
                                maxPoint[1] + i * shipLine[1])
                if isValidPoint(possibleShot):
                    possibleLocations.append(possibleShot)

                possibleShot = (maxPoint[0] - i * shipLine[0],
                                maxPoint[1] - i * shipLine[1])
                if isValidPoint(possibleShot):
                    possibleLocations.append(possibleShot)

            self.killMats[shipName] = set(possibleLocations)

        else:
            # Build out the full kill matrix
            for direction in SHIP_ORIENTATIONS:
                vector = (VECTOR_DICT[direction][0],
                          VECTOR_DICT[direction][1])
                possibleShot = (shot[0] + vector[0], shot[1] + vector[1])
                if isValidPoint(possibleShot):
                    self.killMats[shipName].add(possibleShot)

        if self.killMats[shipName]:
            self.offense = DESTROY

    def shipSunk(self, shipName):
        self.killMats[shipName] = set()

        for killMat in self.killMats.itervalues():
            if killMat:
                self.offense = DESTROY
                break
        else:
            self.offense = SEARCH

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

    def getRandomShot(self):
        shot = (random.randint(0, BOARD_WIDTH - 1),
                random.randint(0, BOARD_HEIGHT - 1))

        while shot in self.shots:
            shot = (random.randint(0, BOARD_WIDTH - 1),
                    random.randint(0, BOARD_HEIGHT - 1))

        return shot

    def fireShot(self):
        shot = None

        while shot is None or shot in self.shots:
            if self.offense == RANDOM:
                shot = self.getRandomShot()
            elif self.offense == DESTROY:
                for killMat in self.killMats.itervalues():
                    if killMat:
                        shot = random.choice(list(killMat))
                        killMat.remove(shot)
                        break
                else:
                    self.offense = SEARCH
            elif self.offense == SEARCH:
                if self.searchMat:
                    shot = random.choice(self.searchMat)
                    self.searchMat.remove(shot)
                else:
                    shot = self.getRandomShot()
                    assert False
        self.shots.add(shot)
        return shot
