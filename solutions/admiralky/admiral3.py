from battlePy.player import Player
from battlePy.ship import (UP,
                           RIGHT,
                           SHIP_ORIENTATIONS,
                           VECTOR_DICT,
                           )
import random, math

(SEARCH,
 DESTROY,
 RANDOM,
 ) = OFFENSIVE_MODES = range(3)

(DEF_RANDOM,
 ADAPTIVE_RANDOM) = DEFENSIVE_MODES = range(2)

def findMinMaxPoint(points):
    minPoint = None
    maxPoint = None
    for point in points:
        if not maxPoint:
            maxPoint = point
        if not minPoint:
            minPoint = point

        if (minPoint[0] > point[0] or
                minPoint[1] > point[1]):
            minPoint = point
        if (maxPoint[0] < point[0] or
                maxPoint[1] < point[1]):
            maxPoint = point
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

def getOneDimensionalDistanceBetweenPoints(shot1, shot2):
    xdiff = abs(shot1[0] - shot2[0])
    ydiff = abs(shot1[1] - shot2[1])
    return max(xdiff, ydiff)

class Admiral3(Player):
    def initPlayer(self, *args, **kwargs):
        self.gameCount = 0
        self.preShotScoreRounds = kwargs.get('preShotScoreRounds', 0)
        useAdaptiveDef = kwargs.get('useAdaptiveDef', True)
        if useAdaptiveDef:
            self.defense = ADAPTIVE_RANDOM
        else:
            self.defense = DEF_RANDOM
        self.pastMisses = {}
        
    def newGame(self):
        self.shipSpecs = self.currentGame.shipSpecs
        self.gameCount += 1

        self.shotsByRow = {}
        self.shotsByColumn = {}

        if not self.pastMisses:
            for i in xrange(self.boardWidth):
                for j in xrange(self.boardHeight):
                    self.pastMisses[(i, j)] = 0

        for i in xrange(self.boardHeight):
            self.shotsByRow[i] = [-1, self.boardWidth]
        for i in xrange(self.boardWidth):
            self.shotsByColumn[i] = [-1, self.boardHeight]

        self.shipSizes = dict(((x[0], x[1]) for x in self.shipSpecs))
        self.remainingShips = dict(((x[0], x[1]) for x in self.shipSpecs))

        self.shots = set()
        self.remainingShots = set([(x, y) for x in xrange(self.boardWidth) for y in xrange(self.boardHeight)])
        self.foundShips = dict(((x[0], []) for x in self.shipSpecs))
        self.searchMat = []
        self.killMats = dict(((x[0], set()) for x in self.shipSpecs))

        self.currentOffense = RANDOM
        self.defaultOffense = RANDOM

        for i in xrange(self.boardHeight):
            for j in xrange(i % 2, self.boardWidth, 2):
                self.searchMat.append((i, j))

    def isPossibleShot(self, shot, minPoint, maxPoint, shipName):
        shipSize = self.shipSizes[shipName]
        hitLocations = self.foundShips[shipName]
        if (self.isValidPoint(shot) and
                abs(maxPoint[0] - shot[0]) < self.shipSizes[shipName] and
                abs(maxPoint[1] - shot[1]) < self.shipSizes[shipName] and
                abs(minPoint[0] - shot[0]) < self.shipSizes[shipName] and
                abs(minPoint[1] - shot[1]) < self.shipSizes[shipName]):
            if shot != minPoint:
                possibleShipLine = normalize((abs(shot[0] - minPoint[0]), abs(shot[1] - minPoint[1])))
            else:
                possibleShipLine = normalize((abs(shot[0] - maxPoint[0]), abs(shot[1] - maxPoint[1])))

            possibleMin, possibleMax = findMinMaxPoint([minPoint, maxPoint, shot])
            maxCandidates = set()
            minCandidates = set()
            for i in xrange(shipSize):
                maxCandidate = (possibleMin[0] + possibleShipLine[0] * i,
                             possibleMin[1] + possibleShipLine[1] * i)
                maxCandidates.add(maxCandidate)

                minCandidate = (possibleMax[0] - possibleShipLine[0] * i,
                             possibleMax[1] - possibleShipLine[1] * i)
                minCandidates.add(minCandidate)

            candidates = sorted(list(minCandidates.union(maxCandidates)))
            candidates = [x for x in candidates if x not in self.shots or x in hitLocations]
            if len(candidates) < shipSize:
                return False

            for idx, val in enumerate(candidates):
                for i in xrange(shipSize):
                    if idx + i + 1 > len(candidates) - 1:
                        continue

                    if getOneDimensionalDistanceBetweenPoints(candidates[idx + i],
                                                              candidates[idx + i + 1]) > 1:
                        break
                else:
                    return True

        return False

    def buildKillMat(self, shot, hitLocations, shipName):
        possibleLocations = set()

        # Filter out impossible locations
        minPoint, maxPoint = findMinMaxPoint(hitLocations)
        if len(hitLocations) > 1:
            shipLine = normalize((maxPoint[0] - minPoint[0],
                                       maxPoint[1] - minPoint[1]))

            for i in xrange(0, self.shipSizes[shipName] + 1):
                candidate = (minPoint[0] - i * shipLine[0],
                                minPoint[1] - i * shipLine[1])
                if self.isPossibleShot(candidate, minPoint, maxPoint, shipName):
                    possibleLocations.add(candidate)

                candidate = (minPoint[0] + i * shipLine[0],
                                minPoint[1] + i * shipLine[1])
                if self.isPossibleShot(candidate, minPoint, maxPoint, shipName):
                    possibleLocations.add(candidate)

                candidate = (maxPoint[0] + i * shipLine[0],
                                maxPoint[1] + i * shipLine[1])
                if self.isPossibleShot(candidate, minPoint, maxPoint, shipName):
                    possibleLocations.add(candidate)

                candidate = (maxPoint[0] - i * shipLine[0],
                                maxPoint[1] - i * shipLine[1])
                if self.isPossibleShot(candidate, minPoint, maxPoint, shipName):
                    possibleLocations.add(candidate)
        else:
            # Build out the full kill matrix
            for direction in SHIP_ORIENTATIONS:
                vector = (VECTOR_DICT[direction][0],
                          VECTOR_DICT[direction][1])
                candidate = (shot[0] + vector[0], shot[1] + vector[1])
                if self.isPossibleShot(candidate, minPoint, maxPoint, shipName):
                    possibleLocations.add(candidate)
        return possibleLocations

    def opponentShot(self, shot):
        self.pastMisses[shot] += 1

    def shotHit(self, shot, shipName):
        self.foundShips[shipName].append(shot)
        hitLocations = set(self.foundShips[shipName])

        self.killMats[shipName] = self.buildKillMat(shot, hitLocations, shipName)

        if self.killMats[shipName]:
            self.currentOffense = DESTROY

    def shotMiss(self, shot):
        pass

    def shipSunk(self, shipName):
        self.remainingShips.pop(shipName)
        self.killMats[shipName] = set()

        for killMat in self.killMats.itervalues():
            if killMat:
                self.currentOffense = DESTROY
                break
        else:
            self.currentOffense = self.defaultOffense

    def placeShips(self):
        if self.defense == DEF_RANDOM:
            for ship in self.ships:
                isValid = False
                while not isValid:
                    orientation = random.choice([UP, RIGHT])
                    if orientation == UP:
                        location = (random.randint(0, self.boardWidth - 1),
                                    random.randint(0, self.boardHeight - 1 - ship.size))
                    else:
                        location = (random.randint(0, self.boardWidth - 1 - ship.size),
                                    random.randint(0, self.boardHeight - 1))
                    ship.placeShip(location, orientation)

                    if self.isShipPlacedLegally(ship):
                        isValid = True
        elif self.defense == ADAPTIVE_RANDOM:
            placement = self.buildPlacements()
            for ship in placement:
                ship.placeShip(*placement[ship])

    def getRandomShot(self):
        if not self.searchMat:
            shot = (random.randint(0, self.boardWidth - 1),
                    random.randint(0, self.boardHeight - 1))

            while shot in self.shots:
                shot = (random.randint(0, self.boardWidth - 1),
                        random.randint(0, self.boardHeight - 1))
        else:
            if len(self.shots) < self.preShotScoreRounds:
                shot = random.choice(self.searchMat)

                while not self.isShipPossibleAtLocation(shot):
                    self.searchMat.remove(shot)
                    shot = random.choice(self.searchMat)
            else:
                shot = self.getHighestScoredShot()

            self.searchMat.remove(shot)
        return shot

    def fireShot(self):
        shot = None

        while shot is None or shot in self.shots:
            try:
                if self.currentOffense == RANDOM:
                    shot = self.getRandomShot()
                elif self.currentOffense == DESTROY:
                    for killMat in self.killMats.itervalues():
                        if killMat:
                            shot = random.choice(list(killMat))
                            killMat.remove(shot)
                            break
                    else:
                        self.currentOffense = self.defaultOffense
                elif self.currentOffense == SEARCH:
                    shot = self.getRandomShot()
            except KeyboardInterrupt:
                import pdb; pdb.set_trace()
        self.shots.add(shot)
        self.shotsByRow[shot[1]].append(shot[0])
        self.shotsByColumn[shot[0]].append(shot[1])
        self.remainingShots.discard(shot)
        return shot

    def intToPoint(self, num):
        x = num % self.boardWidth
        y = num / self.boardWidth
        return x, y

    def pointToInt(self, point):
        total = point[0] + self.boardWidth * point[1]
        return total

    def isValidPoint(self, point):
        return (0 <= point[0] < self.boardWidth and
                0 <= point[1] < self.boardHeight)

    def isShipPossibleAtLocation(self, shot):
        smallestRemainingShip = min(self.remainingShips.items(), key=lambda x: x[1])

        rowShots = self.shotsByRow[shot[1]]
        columnShots = self.shotsByColumn[shot[0]]

        lowerColumnShot = -1
        upperColumnShot = self.boardWidth

        for x in rowShots:
            if x < shot[0]:
                lowerColumnShot = max(x, lowerColumnShot)
            if x > shot[0]:
                upperColumnShot = min(x, upperColumnShot)

        lowerRowShot = -1
        upperRowShot = self.boardHeight

        for y in columnShots:
            if y < shot[1]:
                lowerRowShot = max(y, lowerRowShot)
            if y > shot[1]:
                upperRowShot = min(y, upperRowShot)

        if (abs(upperColumnShot - lowerColumnShot) > smallestRemainingShip[1] or
                abs(upperRowShot - lowerRowShot) > smallestRemainingShip[1]):
            return True
        else:
            return False

    def score(self, shot):
        total = 0

        if shot in self.shots:
            return total

        rowShots = self.shotsByRow[shot[1]]
        columnShots = self.shotsByColumn[shot[0]]

        lowerColumnShot = -1
        upperColumnShot = self.boardWidth

        for x in rowShots:
            if x < shot[0]:
                lowerColumnShot = max(x, lowerColumnShot)
            if x > shot[0]:
                upperColumnShot = min(x, upperColumnShot)

        lowerRowShot = -1
        upperRowShot = self.boardHeight

        for y in columnShots:
            if y < shot[1]:
                lowerRowShot = max(y, lowerRowShot)
            if y > shot[1]:
                upperRowShot = min(y, upperRowShot)

        for ship in self.remainingShips.items():
            if abs(upperColumnShot - lowerColumnShot) > ship[1]:
                total += 1

            if abs(upperRowShot - lowerRowShot) > ship[1]:
                total += 1

        return total

    def getHighestScoredShot(self):
        scoreMat = dict()
        for shot in self.searchMat:
            scoreMat.setdefault(self.score(shot), []).append(shot)

        sortedScoreMat = sorted(scoreMat.items(), key=lambda x: x[0], reverse=True)
        return random.choice(sortedScoreMat[0][1])

    def scoreShipPlacement(self, placement):
        ''' placement should be a dict containing ships as keys and (location, orientation) as values '''
        total = 0
        for ship in placement:
            locations = self.getLocations(ship, placement[ship])

            for location in locations:
                total += self.pastMisses[location]
        return total

    def getLocations(self, ship, position):
        locations = set()
        refLocation = position[0]
        orientation = position[1]
        locations.add(refLocation)
        for i in xrange(ship.size - 1):
            newLocation = (refLocation[0] + VECTOR_DICT[orientation][0],
                    refLocation[1] + VECTOR_DICT[orientation][1])
            locations.add(newLocation)
        return locations

    def generatePlacement(self):
        allLocations = set()
        placement = dict()
        for ship in self.ships:
            isValid = False
            while not isValid:
                orientation = random.choice([UP, RIGHT])
                if orientation == UP:
                    refLocation = (random.randint(0, self.boardWidth - 1),
                                random.randint(0, self.boardHeight - 1 - ship.size))
                else:
                    refLocation = (random.randint(0, self.boardWidth - 1 - ship.size),
                                random.randint(0, self.boardHeight - 1))
                locations = self.getLocations(ship, (refLocation, orientation))

                for location in locations:
                    if location in allLocations or not self.isValidPoint(location):
                        isValid = False
                        break
                else:
                    isValid = True
                    allLocations = allLocations.union(locations)
                    placement[ship] = (refLocation, orientation) 

        return placement

    def buildPlacements(self):
        placements = [self.generatePlacement() for i in xrange(100)]
        scores = {}
        for placement in placements:
            score = self.scoreShipPlacement(placement)
            scores.setdefault(score, []).append(placement)

        sortedPlacements = sorted(scores.items(), key=lambda x: x[0], reverse=False)
        return random.choice(sortedPlacements[0][1])

Agent = Admiral3
