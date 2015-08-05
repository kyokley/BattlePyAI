import operator

from collections import defaultdict
from battlePy.player import Player
from battlePy.default_config import (BOARD_WIDTH, BOARD_HEIGHT)
from battlePy.ship import UP, RIGHT

class MoveUp(object):
    @staticmethod
    def next(hits, misses, shot):
        x, y = shot
        while True:
            y = y + 1
            next_shot = x, y
            if next_shot[1] > BOARD_HEIGHT - 1 or next_shot in misses:
                # off edge of board or ship
                return None
            if next_shot not in hits:
                return next_shot


class MoveDown(object):
    @staticmethod
    def next(hits, misses, shot):
        x, y = shot
        while True:
            y = y - 1
            next_shot = x, y
            if next_shot[1] < 0 or next_shot in misses:
                # off edge of board or ship
                return None
            if next_shot not in hits:
                return next_shot


class MoveLeft(object):
    @staticmethod
    def next(hits, misses, shot):
        x, y = shot
        while True:
            x = x - 1
            next_shot = x, y
            if x < 0 or next_shot in misses:
                # off edge of board or ship
                return None
            if next_shot not in hits:
                return next_shot


class MoveRight(object):
    @staticmethod
    def next(hits, misses, shot):
        x, y = shot
        while True:
            x = x + 1
            next_shot = x, y
            if x > BOARD_WIDTH - 1 or next_shot in misses:
                # off edge of board or ship
                return None
            if next_shot not in hits:
                return next_shot


class OldAgeAndTreachery(Player):

    def initPlayer(self, *args, **kwargs):
        self.name = 'OAAT'
        # history of all games
        self.hit_history = defaultdict(int)
        self._shot_grid = []
        # X.X.X.X.X.
        # .X.X.X.X.X
        # X.X.X.X.X.
        # .X.X.X.X.X
        # X.X.X.X.X.
        # .X.X.X.X.X
        # X.X.X.X.X.
        # .X.X.X.X.X
        # X.X.X.X.X.
        # .X.X.X.X.X
        self._shot_random = []

        for x in range(0, BOARD_WIDTH):
            for y in range(0, BOARD_HEIGHT):
                if (y % 2 == 0 and x % 2 == 1) or (y % 2 == 1 and x % 2 == 0):
                    self._shot_grid.append((x, y))
                self._shot_random.append((x, y))
        self._last_placements_right = {}
        self._last_placements_up = {}
        self._game_number = -1

    def newGame(self):
        self._game_number += 1
        self.shots = set()
        self.misses = set()
        self.hits = set()
        self.last_hit = None
        self.last_direction = MoveRight
        self.last_shot_status = False
        # sort by most hits ascending
        self.shots_by_frequency = [x[0] for x in sorted(self.hit_history.items(), key=operator.itemgetter(1), reverse=True) if x[1] > 0]
        self.shot_grid = list(self._shot_grid)
        self.shot_random = list(self._shot_random)

    def placeShips(self):
        for i, ship in enumerate(self.ships):
            isValid = False
            while not isValid:
                location, orientation = self._place_ship_distributed(ship, i)
                ship.placeShip(location, orientation)

                if self.isShipPlacedLegally(ship):
                    isValid = True
                    if orientation is UP:
                        self._last_placements_up[ship.name] = location, orientation
                    else:
                        self._last_placements_right[ship.name] = location, orientation

    def _place_ship_centered(self, ship, i):
        orientation = RIGHT
        location = (BOARD_WIDTH - ship.size) // 2, i * 2
        return location, orientation

    def _place_ship_distributed(self, ship, i):
        variant = self._game_number % 4
        if variant in (0, 1):
            orientation = RIGHT
            if ship.name not in self._last_placements_right:
                # first RIGHT game
                return self._place_ship_centered(ship, i)
            location, orientation = self._last_placements_right[ship.name]
            if variant == 1:
                # leave x increment y
                y = location[1] + 1
                if y > BOARD_HEIGHT - 1:
                    y = 0
                location = location[0], y
            else:
                # leave y increment x
                x = location[0] + 1
                if x + ship.size - 1 > BOARD_WIDTH - 1:
                    x = 0
                location = x, location[1]
        else:
            orientation = UP
            if ship.name not in self._last_placements_up:
                # first UP game
                (y, x), old_orientation = self._place_ship_centered(ship, i)
                return (x, y), orientation
            location, orientation = self._last_placements_up[ship.name]
            if variant == 2:
                # leave y increment x
                x = location[0] + 1
                if x > BOARD_WIDTH - 1:
                    x = 0
                location = x, location[1]
            else:
                # leave x increment y
                y = location[1] + 1
                if y + ship.size - 1 > BOARD_HEIGHT - 1:
                    y = 0
                location = location[0], y
        return location, orientation

    def fireShot(self):
        shot = None
        if self.last_hit is None:
            shot = self._shoot_historically()
        else:
            # search near our last hit
            if self.last_direction in (MoveLeft, MoveRight):
                shot = self._shoot_horizontally()
                if shot is None:
                    shot = self._shoot_vertically()
            else:
                shot = self._shoot_vertically()
                if shot is None:
                    shot = self._shoot_horizontally()
            if shot is None:
                shot = self._shoot_historically()
        self.shots.add(shot)
        return shot

    def _shoot_randomly(self):
        try:
            while True:
                shot = self.shot_random.pop()
                if shot not in self.shots:
                    return shot
        except IndexError:
            shot = None
        return shot

    def _shoot_grid(self):
        try:
            while True:
                shot = self.shot_grid.pop()
                if shot not in self.shots:
                    return shot
        except IndexError:
            shot = self._shoot_randomly()
        return shot

    def _shoot_historically(self):
        try:
            while True:
                shot = self.shots_by_frequency.pop()
                if shot not in self.shots:
                    return shot
        except IndexError:
            shot = self._shoot_grid()
        return shot

    def _shoot_horizontally(self):
        if self.last_shot_status is False:
            # missed so go back to last hit
            # and see if we have space in the other direction
            # that we haven't tried yet
            self.last_direction = self.last_direction == MoveLeft and MoveRight or MoveLeft
        return self.last_direction.next(self.hits, self.misses, self.last_hit)

    def _shoot_vertically(self):
        if self.last_shot_status is False:
            # miss so go back to last hit
            # see if we have space in the other direction
            # that we haven't tried yet
            self.last_direction = self.last_direction == MoveUp and MoveDown or MoveUp
        return self.last_direction.next(self.hits, self.misses, self.last_hit)

    def shotHit(self, shot, shipName):
        ''' Method called when a ship is hit

        Args:
            shot (tuple): x, y pair of the shot location
            shipName (string): Name of the ship that was hit
        '''
        self.hits.add(shot)
        self.last_shot_status = True
        self.last_hit = shot
        self.hit_history[shot] += 1

    def shotMissed(self, shot):
        ''' Method called when a shot misses

        Args:
            shot (tuple): x, y pair of the shot location
        '''
        self.misses.add(shot)
        self.last_shot_status = False
        self.hit_history[shot] -= 1
