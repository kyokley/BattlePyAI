from battlePy.player import Player
from battlePy.ship import UP, RIGHT
import random

HUNT = 1
KILL = 2

SIDE_UP = 0
SIDE_DOWN = 1
SIDE_LEFT = 2
SIDE_RIGHT = 3

SHIP_CARRIER = 0;
SHIP_BATTLESHIP = 1;
SHIP_DESTROYER = 2;
SHIP_SUBMARINE = 3;
SHIP_PATROL = 4;

def strToType(str):
    if str == 'Carrier':
        return SHIP_CARRIER
    elif str == 'Battleship':
        return SHIP_BATTLESHIP
    elif str == 'Destroyer':
        return SHIP_DESTROYER
    elif str == 'Submarine':
        return SHIP_SUBMARINE
    elif str == 'Patrol Boat':
        return SHIP_PATROL
    else:
        raise ValueError('unknown ship name' + str)


class ShotList:

    def __init__(self, width, height, shotsFired, stype):
        self.shots = []
        self.stype = stype

        offset = self.typeToNum(stype)
        currOffset = offset - 1
        for y in range(height):
            x = currOffset
            if currOffset > 0:
                currOffset -= 1
            else:
                currOffset = offset - 1
                
            while x < width:
                if not (x, y) in shotsFired:
                    self.shots.append((x, y))
                x += offset

        random.shuffle(self.shots)


    def typeToNum(self, stype):
        if stype == SHIP_CARRIER:
            return 5
        elif stype == SHIP_BATTLESHIP:
            return 4
        elif stype == SHIP_DESTROYER:
            return 3
        elif stype == SHIP_SUBMARINE:
            return 3
        elif stype == SHIP_PATROL:
            return 2



    
    def pop(self):
        return self.shots.pop()

    def remove(self, space):
        self.shots.remove(space)

    def contains(self, space):
        return space in self.shots

    def empty(self):
        return len(self.shots) == 0
    

class TargetArea:

    def __init__(self, width, height, stype, space, shots, shotsFired):
        self.stype = stype
        self.width = width
        self.height = height
        self.shots = shots;
        self.shotsFired = shotsFired;
        self.sides = self.getSurroundingArea(space)
        self.isSunk = False

    def getSurroundingArea(self, space):
        surroundings = []
        up = []
        sides = [[],[],[],[]]

        for y in range(space[1] + 1, space[1] + 5):
            if (space[0], y) not in self.shotsFired:
                if y >= 0 and y < self.height:
                    up.append((space[0], y))
            else:
                break

        down = []

        for y in reversed(range(space[1] - 4, space[1])):
            if (space[0], y) not in self.shotsFired:
                if y >= 0 and y < self.height:
                    down.append((space[0], y))
            else:
                break

        right = []

        for x in range(space[0] + 1, space[0] + 5):
            if (x, space[1]) not in self.shotsFired:
                if x >= 0 and x < self.width:
                    right.append((x, space[1]))
            else:
                break

        left = []

        for x in reversed(range(space[0] - 4, space[0])):
            if (x, space[1]) not in self.shotsFired:
                if x >= 0 and x < self.width:
                    left.append((x, space[1]))
            else:
                break

        sides[SIDE_UP] = up
        sides[SIDE_DOWN] = down
        sides[SIDE_LEFT] = left
        sides[SIDE_RIGHT] = right

        for idx, side in enumerate(sides):
            if len(side) == 0:
                sides[idx] = None

        return sides;

    def getShot(self):
        for side in self.sides:
            if not side is None:
                for space in side:
                    if space not in self.shotsFired:
                        return space

        raise Exception('exc')

    def hit(self, space, stype):

        for idx, side in enumerate(self.sides):
            if not side is None:
                if space in side:
                    if self.stype == stype:
                        if idx == SIDE_UP or idx == SIDE_DOWN:
                            self.sides[SIDE_LEFT] = None
                            self.sides[SIDE_RIGHT] = None
                        else:     
                            self.sides[SIDE_UP] = None
                            self.sides[SIDE_DOWN] = None
                        side.remove(space)
                        if len(side) == 0:
                            self.sides[idx] = None
                    else:
                        self.sides[idx] = None

    def miss(self, space):
        for idx, side in enumerate(self.sides):
            if not side is None and space in side:
                self.sides[idx] = None


    def destroyed(self):
        if self.isSunk:
            return True

        for side in self.sides:
            if not side is None:
                return False
            
        return True

    def sunk(self, stype):
        if self.stype == stype:
            self.isSunk = True
    
class AdmiralNelson(Player):
    def initPlayer(self, *args, **kwargs):
        self.name = 'Admiral Nelson'

    def newGame(self):
        self.shipsToSeek = [SHIP_PATROL, SHIP_SUBMARINE, SHIP_DESTROYER, SHIP_BATTLESHIP, SHIP_CARRIER]
        self.shipsSunk = []

        self.sunk = []
        self.mode = HUNT
        self.target = None

        height = self.currentGame.boardHeight
        width = self.currentGame.boardWidth

        self.shotsFired = [];
        self.shots = ShotList(width, height, self.shotsFired, self.shipsToSeek.pop())
        

        self.killstack = []
        pass

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
        if self.target != None and self.target.destroyed():
            self.mode = HUNT

        height = self.currentGame.boardHeight
        width = self.currentGame.boardWidth

        if self.mode == HUNT and len(self.killstack) != 0:
            while len(self.killstack) != 0:
                shipPart = self.killstack.pop()
                target = TargetArea(width, height, shipPart[1], shipPart[0], self.shots.shots, self.shotsFired)
                if not target.destroyed(): 
                    self.target = target;
                    self.mode = KILL
                    break;


        if self.mode == HUNT:
            #if self.shots.empty() or (self.shots.stype in self.shipsSunk):
            if self.shots.stype in self.shipsSunk:
                self.shots = ShotList(width, height, self.shotsFired, self.shipsToSeek.pop())
            return self.shots.pop()
        elif self.mode == KILL:
            return self.target.getShot()

    def shotHit(self, shot, shipName):
        stype = strToType(shipName)

        if self.target != None and self.target.stype != stype:
            self.killstack.append((shot, stype))  

        if self.shots.contains(shot):
            self.shots.remove(shot)

        height = self.currentGame.boardHeight
        width = self.currentGame.boardWidth

        if self.mode == HUNT:
            self.target = TargetArea(width, height, stype, shot, self.shots.shots, self.shotsFired)
            self.mode = KILL
        else:
            self.target.hit(shot, stype)
        pass
        self.shotsFired.append(shot);

    def shotMissed(self, shot):
        if self.shots.contains(shot):
            self.shots.remove(shot)

        if self.mode == KILL:
            self.target.miss(shot)

        self.shotsFired.append(shot);
        pass

    def shipSunk(self, shipName):
        stype = strToType(shipName)
        self.sunk.append(stype)
        if not self.target is None:
            self.target.sunk(stype)

        if stype in self.shipsToSeek:
            self.shipsToSeek.remove(stype)


        self.shipsSunk.append(stype)



Agent = AdmiralNelson
