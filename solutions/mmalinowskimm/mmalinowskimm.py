from battlePy.player import Player
from battlePy.default_config import (BOARD_WIDTH,
                                     BOARD_HEIGHT)
from battlePy.ship import UP, RIGHT
import random
from random import shuffle


class Mmalinowski(Player):

    def initPlayer(self):
        self.name = 'mmalinowski'
        self.gameCount = 0
        if BOARD_WIDTH == 10 and BOARD_HEIGHT == 10:
            self.sumBaseMap = [[0.037653740000000005,
                                0.05647634,
                                0.06981358,
                                0.07437440000000001,
                                0.07607968000000001,
                                0.0760353,
                                0.07434505999999999,
                                0.06989612,
                                0.05665612,
                                0.03768052],
                               [0.05641452,
                                0.0752512,
                                0.08863856,
                                0.09312132000000001,
                                0.0948564,
                                0.09482431999999999,
                                0.09313368,
                                0.08859679999999999,
                                0.07536888,
                                0.05655926],
                               [0.0697335,
                                0.08856622,
                                0.10188704,
                                0.10634236,
                                0.10805005999999999,
                                0.10802890000000001,
                                0.10656760000000001,
                                0.10190664,
                                0.08861802,
                                0.06989168],
                               [0.07432878,
                                0.09304710000000001,
                                0.10633437999999999,
                                0.11094878,
                                0.11253914000000001,
                                0.11246573999999998,
                                0.11084152,
                                0.10644676,
                                0.09320737999999999,
                                0.074401],
                               [0.07606850000000001,
                                0.09477680000000001,
                                0.10807989999999998,
                                0.11250446,
                                0.11415858000000001,
                                0.11413762000000001,
                                0.11252569999999999,
                                0.10806441999999998,
                                0.09482672,
                                0.07595024],
                               [0.07601625999999999,
                                0.09482208,
                                0.1080646,
                                0.11253758,
                                0.1141343,
                                0.11417606,
                                0.11248632,
                                0.10817244000000001,
                                0.09487444,
                                0.0759641],
                               [0.07416061999999998,
                                0.09298774,
                                0.10644266,
                                0.11092024,
                                0.11258208,
                                0.11250157999999999,
                                0.11099803999999999,
                                0.10654388,
                                0.09328242,
                                0.07435130000000001],
                               [0.06970327999999999,
                                0.0885959,
                                0.10188744000000001,
                                0.106226,
                                0.10804158,
                                0.10799444,
                                0.1063444,
                                0.10174254,
                                0.08846924,
                                0.06961421999999999],
                               [0.05645177999999999,
                                0.07529612,
                                0.0885338,
                                0.09305416000000001,
                                0.09479291999999999,
                                0.09483664,
                                0.09306041999999999,
                                0.08850105999999999,
                                0.07530056,
                                0.056379460000000006],
                               [0.0375954,
                                0.056543460000000004,
                                0.0698511,
                                0.07437886,
                                0.07598730000000001,
                                0.07602856,
                                0.07415770000000001,
                                0.0696263,
                                0.056411140000000005,
                                0.03755414]]
            self.origBaseMap = [x[:] for x in self.sumBaseMap]
        else:
            self.sumBaseMap = [[0] * BOARD_WIDTH for i in range(0, BOARD_HEIGHT)]
            self.origBaseMap = [[0] * BOARD_WIDTH for i in range(0, BOARD_HEIGHT)]

    def newGame(self):
        self.hitCarrier = False
        self.hitSubmarine = False
        self.hitPatrolBoat = False
        self.hitDestroyer = False
        self.hitBattleship = False
        self.shots = []
        self.miss = []
        self.hits = []
        self.infoMatrix = {}

        self.infoMatrix['m'] = [[0] * (BOARD_WIDTH)
                                for i in range(0, BOARD_HEIGHT)]
        self.infoMatrix['h'] = [[0] * (BOARD_WIDTH)
                                for i in range(0, BOARD_HEIGHT)]
        self.infoMatrix['b'] = [[0] * (BOARD_WIDTH)
                                for i in range(0, BOARD_HEIGHT)]
        self.infoMatrix['c'] = [[0] * (BOARD_WIDTH)
                                for i in range(0, BOARD_HEIGHT)]
        self.infoMatrix['d'] = [[0] * (BOARD_WIDTH)
                                for i in range(0, BOARD_HEIGHT)]
        self.infoMatrix['s'] = [[0] * (BOARD_WIDTH)
                                for i in range(0, BOARD_HEIGHT)]
        self.infoMatrix['p'] = [[0] * (BOARD_WIDTH)
                                for i in range(0, BOARD_HEIGHT)]

        self.sumMap = [[0] * (BOARD_WIDTH)
                       for i in range(0, BOARD_HEIGHT)]
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                self.sumMap[y][x] = self.sumBaseMap[y][x]

        self.carrier = True
        self.battleship = True
        self.destroyer = True
        self.submarine = True
        self.patrolBoat = True
        self.r = [[], []]
        self.r[0] = range(0, BOARD_WIDTH, 2)
        self.r[1] = range(1, BOARD_WIDTH, 2)
        self.seededRandom = []
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if x in self.r[y % 2]:
                    self.seededRandom.append((x, y))
        self.seededRandomFallback = []
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if x in self.r[(y + 1) % 2]:
                    self.seededRandomFallback.append((x, y))
        shuffle(self.seededRandom)
        shuffle(self.seededRandomFallback)

    def updateSumBaseMap(self):
        self.gameCount += 1
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if (x, y) in self.hits:
                    self.sumBaseMap[y][x] = float(self.sumBaseMap[y][x] * (
                        10000000 + self.gameCount - 1) + 100) / float(10000000 + self.gameCount)
                else:
                    self.sumBaseMap[y][x] = float(self.sumBaseMap[y][x] * (
                        10000000 + self.gameCount - 1)) / float(10000000 + self.gameCount)
        if self.gameCount % 1000 == 0:
            for y in range(0, BOARD_HEIGHT):
                for x in range(0, BOARD_WIDTH):
                    self.sumBaseMap[y][x] += self.origBaseMap[y][x]
                    self.sumBaseMap[y][x] /= 2

    def gameWon(self):
        self.updateSumBaseMap()

    def gameLost(self):
        self.updateSumBaseMap()

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

    def addShotToMap(self, shot):
        self.shots.append(shot)
        x = shot[0]
        y = shot[1]
        self.infoMatrix['c'][y][x] = 0
        self.infoMatrix['b'][y][x] = 0
        self.infoMatrix['d'][y][x] = 0
        self.infoMatrix['s'][y][x] = 0
        self.infoMatrix['p'][y][x] = 0

        self.updateSumMap()

    def scanSpaces(self, ship, x, y):
        self.infoMatrix[ship] = [[0] * (BOARD_WIDTH)
                                 for i in range(0, BOARD_HEIGHT)]
        for j in range(1, BOARD_HEIGHT - 1):
            if (self.infoMatrix['h'][j + 1][x] == ship and
                    self.infoMatrix['h'][j][x] == ship):
                self.infoMatrix[ship][j - 1][x] = .5

            if (self.infoMatrix['h'][j - 1][x] == ship and
                    self.infoMatrix['h'][j][x] == ship):
                self.infoMatrix[ship][j + 1][x] = .5

        for i in range(1, BOARD_WIDTH - 1):
            if (self.infoMatrix['h'][y][i - 1] == ship and
                    self.infoMatrix['h'][y][i] == ship):
                self.infoMatrix[ship][y][i + 1] = .5

            if (self.infoMatrix['h'][y][i + 1] == ship and
                    self.infoMatrix['h'][y][i] == ship):
                self.infoMatrix[ship][y][i - 1] = .5

    def addHitToMap(self, shot, hitShip):
        x = shot[0]
        y = shot[1]
        if hitShip == "Carrier":
            self.infoMatrix['h'][y][x] = 'c'
            self.infoMatrix['c'][y][x] = 0
            if not self.hitCarrier:
                self.hitCarrier = True
                if x - 4 > -1:
                    for a in range(1, 5):
                        self.infoMatrix['c'][y][x - a] += .25 / (4 * a)
                if x + 4 < BOARD_WIDTH:
                    for a in range(1, 5):
                        self.infoMatrix['c'][y][x + a] += .25 / (4 * a)
                if y - 4 > -1:
                    for a in range(1, 5):
                        self.infoMatrix['c'][y - a][x] += .25 / (4 * a)
                if y + 4 < BOARD_HEIGHT:
                    for a in range(1, 5):
                        self.infoMatrix['c'][y + a][x] += .25 / (4 * a)
            else:
                self.scanSpaces('c', x, y)
        if hitShip == "Destroyer":
            self.infoMatrix['h'][y][x] = 'd'
            self.infoMatrix['d'][y][x] = 0
            if not self.hitDestroyer:
                self.hitDestroyer = True
                if x - 2 > -1:
                    for a in range(1, 3):
                        self.infoMatrix['d'][y][x - a] += .25 / (4 * a)
                if x + 2 < BOARD_WIDTH:
                    for a in range(1, 3):
                        self.infoMatrix['d'][y][x + a] += .25 / (4 * a)
                if y - 2 > -1:
                    for a in range(1, 3):
                        self.infoMatrix['d'][y - a][x] += .25 / (4 * a)
                if y + 2 < BOARD_HEIGHT:
                    for a in range(1, 3):
                        self.infoMatrix['d'][y + a][x] += .25 / (4 * a)
            else:
                self.scanSpaces('d', x, y)
        if hitShip == "Submarine":
            self.infoMatrix['h'][y][x] = 's'
            self.infoMatrix['s'][y][x] = 0
            if not self.hitSubmarine:
                self.hitSubmarine = True
                if x - 2 > -1:
                    for a in range(1, 3):
                        self.infoMatrix['s'][y][x - a] += .25 / (4 * a)
                if x + 2 < BOARD_WIDTH:
                    for a in range(1, 3):
                        self.infoMatrix['s'][y][x + a] += .25 / (4 * a)
                if y - 2 > -1:
                    for a in range(1, 3):
                        self.infoMatrix['s'][y - a][x] += .25 / (4 * a)
                if y + 2 < BOARD_HEIGHT:
                    for a in range(1, 3):
                        self.infoMatrix['s'][y + a][x] += .25 / (4 * a)
            else:
                self.scanSpaces('s', x, y)
        if hitShip == "Battleship":
            self.infoMatrix['h'][y][x] = 'b'
            self.infoMatrix['b'][y][x] = 0
            if not self.hitBattleship:
                self.hitBattleship = True
                if x - 3 > -1 and self.battleship:
                    for a in range(1, 4):
                        self.infoMatrix['b'][y][x - a] += .25 / (4 * a)
                if x + 3 < BOARD_WIDTH:
                    for a in range(1, 4):
                        self.infoMatrix['b'][y][x + a] += .25 / (4 * a)
                if y - 3 > -1:
                    for a in range(1, 4):
                        self.infoMatrix['b'][y - a][x] += .25 / (4 * a)
                if y + 3 < BOARD_HEIGHT:
                    for a in range(1, 4):
                        self.infoMatrix['b'][y + a][x] += .25 / (4 * a)
            else:
                self.scanSpaces('b', x, y)

        if hitShip == "Patrol Boat":
            self.infoMatrix['h'][y][x] = 'p'
            self.infoMatrix['p'][y][x] = 0
            if not self.hitPatrolBoat:
                self.hitPatrolBoat = True
                if x - 1 > -1 and self.patrolBoat:
                    self.infoMatrix['p'][y][x - 1] += .25
                if x + 1 < BOARD_WIDTH:
                    self.infoMatrix['p'][y][x + 1] += .25
                if y - 1 > -1:
                    self.infoMatrix['p'][y - 1][x] += .25
                if y + 1 < BOARD_HEIGHT:
                    self.infoMatrix['p'][y + 1][x] += .25
            else:
                self.scanSpaces('p', x, y)

        self.updateSumMap()

    def updateSumMap(self):

        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                self.sumMap[y][x] = (
                    self.sumBaseMap[y][x] +
                    self.infoMatrix['c'][y][x] +
                    self.infoMatrix['b'][y][x] +
                    self.infoMatrix['s'][y][x] +
                    self.infoMatrix['d'][y][x] +
                    self.infoMatrix['p'][y][x]
                )

                if x > -1 and x < BOARD_WIDTH - 2 and y > -1 and y < BOARD_HEIGHT - 2:
                    if (self.infoMatrix['m'][y - 1][x] == 1 and
                            self.infoMatrix['m'][y + 1][x] == 1 and
                            self.infoMatrix['m'][y][x + 1] == 1 and
                            self.infoMatrix['m'][y][x - 1] == 1):
                        self.sumMap[y][x] = 0

        for i in self.shots:
            self.sumMap[i[1]][i[0]] = 0

    def getShot(self):
        maxi = (0, 0, 0)
        pshots = []
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if self.sumMap[y][x] > maxi[2]:
                    maxi = (x, y, self.sumMap[y][x])
        for y in range(0, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH):
                if round(self.sumMap[y][x], 3) >= round(maxi[2], 3):
                    pshots.append((x, y))
        if len(pshots) > 1:
            t = pshots[random.randint(0, len(pshots) - 1)]
            maxi = (t[0], t[1], maxi[2])
        if round(maxi[2], 3) > round(self.sumBaseMap[maxi[1]][maxi[0]], 3):
            return (maxi[0], maxi[1])

        else:
            shot = self.seededRandom[0]
            cc = 0
            for s in self.seededRandom:
                if s not in self.shots:
                    shot = s
            if shot in self.shots:
                return (maxi[0], maxi[1])

            while shot in self.shots:
                cc += 1
                if cc > 49:
                    shot = (maxi[0], maxi[1])
                else:
                    shot = self.seededRandom[cc]

            return shot

    def fireShot(self):
        x = self.getShot()
        self.addShotToMap(x)
        return x

    def shotHit(self, shot, hitShip):
        self.hits.append(shot)
        self.addHitToMap(shot, hitShip)

    def shipSunk(self, hitShip):
        if hitShip == "Carrier":
            self.carrier = False
            self.infoMatrix['c'] = [[0] * BOARD_WIDTH for i in range(0, BOARD_HEIGHT)]
        if hitShip == "Destroyer":
            self.destroyer = False
            self.infoMatrix['d'] = [[0] * BOARD_WIDTH for i in range(0, BOARD_HEIGHT)]
        if hitShip == "Submarine":
            self.submarine = False
            self.infoMatrix['s'] = [[0] * BOARD_WIDTH for i in range(0, BOARD_HEIGHT)]
        if hitShip == "Battleship":
            self.battleship = False
            self.infoMatrix['b'] = [[0] * BOARD_WIDTH for i in range(0, BOARD_HEIGHT)]
        if hitShip == "Patrol Boat":
            self.patrolBoat = False
            self.infoMatrix['p'] = [[0] * BOARD_WIDTH for i in range(0, BOARD_HEIGHT)]
        self.updateSumMap()

    def checkShip(self, ship):
        if ship == 'c':
            return self.carrier
        if ship == 'b':
            return self.battleship
        if ship == 's':
            return self.submarine
        if ship == 'd':
            return self.destroyer
        if ship == 'p':
            return self.patrolBoat

    def shotMissed(self, shot):
        self.miss.append(shot)
        x = shot[0]
        y = shot[1]
        self.infoMatrix['m'][y][x] = 1
        try:
            if (y - 1 > -1 and y + 1 < BOARD_HEIGHT - 1 and
                    self.infoMatrix['h'][y - 1][x] != 0 and
                    self.checkShip(self.infoMatrix['h'][y - 1][x])):
                self.infoMatrix[self.infoMatrix['h'][y - 1][x]][
                    y + 1][x] = self.sumBaseMap[y + 1][x]

            if (y - 1 > -1 and y + 1 < BOARD_HEIGHT - 1 and
                    self.infoMatrix['h'][y + 1][x] != 0 and
                    self.checkShip(self.infoMatrix['h'][y + 1][x])):
                self.infoMatrix[self.infoMatrix['h'][y + 1][x]][
                    y - 1][x] = self.sumBaseMap[y - 1][x]

            if (x - 1 > -1 and x + 1 < BOARD_WIDTH - 1 and
                    self.infoMatrix['h'][y][x - 1] != 0 and
                    self.checkShip(self.infoMatrix['h'][y][x - 1])):
                self.infoMatrix[self.infoMatrix['h'][y][x - 1]][
                    y][x + 1] = self.sumBaseMap[y][x + 1]

            if (x - 1 > -1 and x + 1 < BOARD_WIDTH - 1 and
                    self.infoMatrix['h'][y][x + 1] != 0 and
                    self.checkShip(self.infoMatrix['h'][y][x + 1])):
                self.infoMatrix[self.infoMatrix['h'][y][x + 1]][
                    y][x - 1] = self.sumBaseMap[y][x - 1]

        except KeyError:
            pass

Agent = Mmalinowski
