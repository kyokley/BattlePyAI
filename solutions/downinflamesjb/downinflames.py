from battlePy.player import Player

# orientations
from battlePy.ship import UP, DOWN, LEFT, RIGHT, VECTOR_DICT
from battlePy.default_config import DEFAULT_SHIPS

import random

DEFAULT_VALUE = 50

NOT_SHOT, HIT, MISS = 0, 1, 2
all_vectors = UP, DOWN, LEFT, RIGHT
corners = [
        ((0,0), (UP, RIGHT)),
        ((0,9), (DOWN, RIGHT)),
        ((9,0), (UP, LEFT)),
        ((9,9), (DOWN, LEFT))
        ]


def logit(msg):
    return
    with open("log.log", "a") as f:
        f.write(str(msg) + "\n")


def fromTo(point, vector, dist=1):
    x, y = point
    vx, vy = vector
    return x+(vx*dist), y+(vy*dist)


class GridNode(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shotResult = NOT_SHOT
        self.value = DEFAULT_VALUE
        self.xRun = None
        self.yRun = None

    def __str__(self):
        return "<GridNode %s,%x>" % (self.x, self.y)

    def __repr__(self):
        return str(self)

    def markShot(self, result):
        self.shotResult = result

class Board(object):
    def __init__(self):
        self.size = 10, 10
        self.nodes = {}
        self.nodesList = []  # flat

        for x in range(10):
            self.nodes.setdefault(x, {})
            for y in range(10):
                gn = GridNode(x,y)
                self.nodes[x][y] = gn 
                self.nodesList.append(gn)

        for node in self.nodesList:
            for vector in all_vectors:
                venum = vector
                vector = VECTOR_DICT[vector]
                xp, yp = fromTo((x,y), vector)

    def isValidSpace(self, x, y):
        if x >= 0 and x < 10:
            if y >= 0 and y < 10:
                return True
        return False

    def nodeAt(self, x, y):
        if self.isValidSpace(x,y):
            return self.nodes[x][y]
        return None



class GameTracker(object):
    def __init__(self):
        self.gamesTracked = 0
        self.gamesWon = 0
        self.gamesLost = 0
        self.speeds = []
    

    def logStatistics(self):
        try:
            ratio = self.gamesWon/float(self.gamesLost)
        except:
            ratio = 1.0
        speed = 0
        if self.speeds:
            speed = sum(self.speeds) / float(len(self.speeds))

        logit("W/L ratio: %s/%s = %.2f" % (self.gamesWon, self.gamesLost, ratio))
        logit("avg win speed: %.2f" % speed) 


class ShipTracker(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.seen = False
        self.dead = False
        self.possible_vectors = [UP, DOWN, LEFT, RIGHT]
        self.known_positions = []
        self.likely_positions = []

class GameState(object):
    def __init__(self):
        self.shot_cells = []
        self.board = Board()

        self.ships = {}
        for name, size in DEFAULT_SHIPS:
            self.ships[name] = ShipTracker(name, size) 

class Run(object):
    def __init__(self):
        self.nodes = []
        self.values = []
        self.baseValue = 10
        self.maxValue = 20

    def insert(self, value):
        self.nodes.append(value)

    def revalue(self, strategy = "ramp"):
        self.values = [self.baseValue for n in self.nodes]

        if strategy == "spliteven":
            if len(self.values) > 2:
                midpoint = len(self.values) / 2
                self.values[midpoint] = self.maxValue
                if len(self.values) % 2 == 0:
                    self.values[midpoint + 1] = self.maxValue

        if strategy == "ramp":
            if len(self.values) > 1:
                size = len(self.values)
                odd = size % 2 != 0
                intby2 = size/2
                if odd: 
                    midpoints = intby2, intby2 
                else:
                    midpoints = intby2, intby2 - 1 
                self.values[midpoints[0]] = self.maxValue
                self.values[midpoints[1]] = self.maxValue
                firstOthers = range(1, midpoints[0])
                lastOthers = range(midpoints[1]+1, size-1)
                lastOthers.reverse()
                for inbetweens in firstOthers, lastOthers:
                    if not inbetweens:
                        continue
                    ibsize = len(inbetweens)
                    increment = (self.maxValue - self.baseValue) / ibsize
                    scale = 0
                    for x in inbetweens:
                        scale += 1
                        self.values[x] += increment * scale 

    def valueFor(self, node):
        return self.values[self.nodes.index(node)]


class DownInFlames(Player):

    def initPlayer(self, *args, **kwargs):
        """Called once per match, not each game."""
        self.name = 'Down In Flames'
        self.tracker = GameTracker()
        self.state = None


    def revalueBoard(self):

        for x in range(10):
            for y in range(10):
                node = self.state.board.nodeAt(x,y)
                node.value = DEFAULT_VALUE

                # do other stuff
                if node.shotResult != NOT_SHOT:
                    node.value = 0
                    node.xRun = None
                    node.yRun = None
                else:
                    # fill in run data as we visit each one
                    down = self.state.board.nodeAt(*fromTo((x,y), VECTOR_DICT[DOWN]))    
                    left = self.state.board.nodeAt(*fromTo((x,y), VECTOR_DICT[LEFT]))    
                    if down and down.yRun:
                        node.yRun = down.yRun
                        node.yRun.insert(node)
                    else:
                        node.yRun = Run()
                        node.yRun.insert(node)
                    if left and left.xRun:
                        node.xRun = left.xRun
                        node.xRun.insert(node)
                    else:
                        node.xRun = Run()
                        node.xRun.insert(node)

        for x in range(10):
            for y in range(10):
                node = self.state.board.nodeAt(x,y)
                if node.xRun and node.yRun:
                    anyFit = False
                    for run in node.xRun, node.yRun:
                        size = len(run.nodes)
                        shipsThatFit = 0
                        for ship in self.state.ships.values():
                            if not ship.seen:
                                if ship.size <= size:
                                    shipsThatFit += 1
                        run.revalue()
                        node.value += run.valueFor(node) * shipsThatFit
                        if shipsThatFit > 0:
                            anyFit = True

                    if not anyFit: 
                        node.value = -1

        # evaluate known ship data, LAST
        for ship in self.state.ships.values():
            if ship.seen and not ship.dead:
                for node in ship.likely_positions:
                    if node.shotResult == NOT_SHOT:
                        node.value = 50000

        self.logBoard()

    def logBoard(self):
        return
        logit("-------------------------")
        for y in range(9,-1,-1):
            ls = ""
            for x in range(0,10,1):
                value = self.state.board.nodeAt(x,y).value
                ls += "%6d " % value
            logit(ls) 

    def chooseShot(self):
        self.state.board.nodesList.sort(key=lambda x: x.value)
        highscore = self.state.board.nodesList[-1].value 
        choices = []
        idx = -1
        while self.state.board.nodesList[idx].value == highscore:
            choices.append(self.state.board.nodesList[idx])
            idx -= 1
            try:
                self.state.board.nodesList[idx]
            except:
                break
        
        random.shuffle(choices)
        choice = choices[0]
        self.state.shot_cells.append(choice)
        return (choice.x, choice.y)

    def newGame(self):
        "called once per game"
        logit("GAME START")
        self.state = GameState()
        self.tracker.gamesTracked += 1

    def placeShips(self):
        badnodes = []
        shipNodes = []

        for ship in sorted(self.ships, key=lambda x: x.size): # self.ships is created by the game engine
            shipNodes = []
            valid = False
            while not valid:
                valid = True
                if ship.size == 2:
                    pos, vectors = random.choice(corners)
                    pos = list(pos)
                    # jitter it
                    if pos[0] == 0:
                        pos[0] += random.randint(0,1)
                    if pos[1] == 0:
                        pos[1] += random.randint(0,1)
                    if pos[0] == 9:
                        pos[0] -= random.randint(0,1)
                    if pos[1] == 9:
                        pos[1] -= random.randint(0,1)
                    pos = tuple(pos)
                    vector = random.choice(vectors)
                else:
                    randnode = random.choice([n for n in self.state.board.nodesList if n not in badnodes])
                    pos = randnode.x, randnode.y
                    vector = random.choice(all_vectors)
                px,py = pos
                shipNodes = [self.state.board.nodeAt(px, py)]
                for x in range(ship.size-1):
                    spotx, spoty = fromTo((shipNodes[-1].x, shipNodes[-1].y), VECTOR_DICT[vector])
                    if not self.state.board.isValidSpace(spotx, spoty):
                        valid = False
                        continue
                    shipNodes.append(self.state.board.nodeAt(spotx, spoty))
                for node in shipNodes:
                    if node in badnodes:
                        valid = False
            badnodes.extend(shipNodes) 
            for shipNode in shipNodes:
                for v in all_vectors:
                    nx, ny = fromTo((shipNode.x, shipNode.y), VECTOR_DICT[v])
                    if self.state.board.isValidSpace(nx, ny):
                        badnodes.append(self.state.board.nodeAt(nx, ny))
            ship.placeShip(pos, vector)
                   

    def fireShot(self):
        """Called once per turn, you must fire"""
        self.revalueBoard()
        return self.chooseShot()

    def shotHit(self, shot, shipName):
        """Called when your shot has hit"""
        x,y = shot
        self.state.board.nodeAt(x, y).markShot(HIT)
        ship = self.state.ships[shipName]
        ship.known_positions.append(self.state.board.nodeAt(x,y))
        if len(ship.known_positions) == 1:
            # eliminate impossible vectors right away, if we can
            # leftright
            RLFree = 0
            nextR = x + 1
            nextL = x - 1
            while nextR < 10 and self.state.board.nodeAt(nextR, y).shotResult == NOT_SHOT:
                nextR += 1
                RLFree += 1
            while nextL >=0 and self.state.board.nodeAt(nextL, y).shotResult == NOT_SHOT:
                nextL -= 1
                RLFree += 1
            if RLFree < ship.size - 1:
                ship.possible_vectors.remove(LEFT)
                ship.possible_vectors.remove(RIGHT)
            #updown
            UDFree = 0
            nextU = y + 1
            nextD = y - 1
            while nextU < 10 and self.state.board.nodeAt(x,nextU).shotResult == NOT_SHOT:
                nextU += 1
                UDFree += 1
            while nextD >=0 and self.state.board.nodeAt(x, nextD).shotResult == NOT_SHOT:
                nextD -= 1
                UDFree += 1
            if UDFree < ship.size - 1:
                ship.possible_vectors.remove(UP)
                ship.possible_vectors.remove(DOWN)

        if len(ship.known_positions) > 1:
            # invalidate impossible vectors 
            a, b = ship.known_positions[0:2]
            to_remove = []
            if a.x == b.x:
                if LEFT in ship.possible_vectors:
                    ship.possible_vectors.remove(LEFT)
                if RIGHT in ship.possible_vectors:
                    ship.possible_vectors.remove(RIGHT)
                for pos in ship.likely_positions:
                    if pos.x != a.x:
                        to_remove.append(pos)

            if a.y == b.y:
                if UP in ship.possible_vectors:
                    ship.possible_vectors.remove(UP)
                if DOWN in ship.possible_vectors:
                    ship.possible_vectors.remove(DOWN)
                for pos in ship.likely_positions:
                    if pos.y != a.y:
                        to_remove.append(pos)
            for badpos in to_remove:
                ship.likely_positions.remove(badpos)

        for v in ship.possible_vectors:
            v = VECTOR_DICT[v]
            newx, newy = fromTo((x,y), v)
            if self.state.board.isValidSpace(newx, newy):
                ship.seen = True
                ship.likely_positions.append(self.state.board.nodeAt(newx, newy))

    def shotMissed(self, shot):
        """Called when your shot has missed"""
        x,y = shot
        self.state.board.nodeAt(x, y).markShot(MISS)

    def opponentShot(self, shot):
        """Called when your opponent shoots"""
        pass

    def shipSunk(self, shipName):
        """Called when you sink a ship."""
        self.state.ships[shipName].dead = True
        self.state.ships[shipName].likely_positions = []

    def gameWon(self):
        """Called when you win."""
        self.tracker.gamesWon += 1
        self.tracker.speeds.append(len(self.state.shot_cells))
        self.tracker.logStatistics()

    def gameLost(self):
        """Called when you lose"""
        self.tracker.gamesLost += 1
        self.tracker.logStatistics()

Agent = DownInFlames
