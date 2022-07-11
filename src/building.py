from constants import *
from colorama import Fore, Back, Style
import time


class Buildings():
    def __init__(self, startX, startY, width, height, health):
        self.isDestroyed = False
        self.X = startX
        self.Y = startY
        self.width = width
        self.height = height
        self.health = health
        self.totalHealth = health
        self.pixel = Back.GREEN
        self.flag = False

    def display(self, GRID):
        if self.isDestroyed == True:
            return

        h = self.health/self.totalHealth
        h = h * 100
        if h > 50:
            self.pixel = Back.GREEN
        elif h > 20:
            self.pixel = Back.YELLOW
        else:
            self.pixel = Back.RED
        if self.flag == True:
            self.pixel += Fore.BLACK
            self.flag = False
        for i in range(self.height):
            for j in range(self.width):
                GRID[self.X+i][self.Y+j] = self.pixel + \
                    self.char + Style.RESET_ALL

    def check_circle_circle_overlap(self, R, Xc, Yc, X1, Y1, X2, Y2):
        Xn = max(X1, min(Xc, X2))
        Yn = max(Y1, min(Yc, Y2))
        Dx = Xn - Xc
        Dy = Yn - Yc
        return (Dx**2 + Dy**2) <= R**2

    def outer_wall_coords(self, obj):
        for i in range(0, ROWS):
            for j in range(0, COLS):
                if i == 0 or i == ROWS-1 or j == 0 or j == COLS-1:
                    obj.append(Walls(i, j, 1, 1, WALL_HEALTH))


class TownHall(Buildings):
    def __init__(self, TOWN_HALL_X, TOWN_HALL_Y,
                 TOWN_HALL_WIDTH, TOWN_HALL_HEIGHT, TOWN_HALL_HEALTH):
        super().__init__(TOWN_HALL_X, TOWN_HALL_Y,
                         TOWN_HALL_WIDTH, TOWN_HALL_HEIGHT, TOWN_HALL_HEALTH)
        self.char = 'T'

    def get_wall_coords(self, wall_X, wall_Y):
        top_X = self.X-2
        top_Y = self.Y-2
        bottom_X = self.X+self.height
        bottom_Y = self.Y+self.width
        for i in range(top_X, bottom_X+2):
            for j in range(top_Y, bottom_Y+10):
                if i == top_X or i == bottom_X+1 or j == top_Y or j == bottom_Y+9:
                    wall_X.append(i)
                    wall_Y.append(j)


class Huts(Buildings):
    def __init__(self, HUTS_X, HUTS_Y, HUTS_WIDTH, HUTS_HEIGHT, HUTS_HEALTH):
        super().__init__(HUTS_X, HUTS_Y, HUTS_WIDTH, HUTS_HEIGHT, HUTS_HEALTH)
        self.char = 'H'


class Walls(Buildings):
    def __init__(self, WALLS_X, WALLS_Y, WALLS_WIDTH, WALLS_HEIGHT, WALLS_HEALTH):
        super().__init__(WALLS_X, WALLS_Y, WALLS_WIDTH, WALLS_HEIGHT, WALLS_HEALTH)
        self.char = 'W'


class Cannon(Buildings):
    def __init__(self, CANNON_X, CANNON_Y, CANNON_WIDTH, CANNON_HEIGHT, CANNON_HEALTH):
        super().__init__(CANNON_X, CANNON_Y, CANNON_WIDTH, CANNON_HEIGHT, CANNON_HEALTH)
        self.char = 'C'
        self.range = CANNON_RANGE
        self.damage = CANNON_DAMAGE

    def shoot(self, army):
        if self.isDestroyed == True:
            return
        for obj in army:
            if obj.isDestroyed == False and self.check_circle_circle_overlap(self.range, self.X+1, self.Y+1, obj.X, obj.Y, obj.X+obj.height, obj.Y+obj.width):
                obj.health -= self.damage
                if obj.health <= 0:
                    obj.isDestroyed = True
                    obj.health = 0
                self.flag = True
                return
        return


class Wizard(Buildings):
    def __init__(self, WIZARD_X, WIZARD_Y, WIZARD_WIDTH, WIZARD_HEIGHT, WIZARD_HEALTH):
        super().__init__(WIZARD_X, WIZARD_Y, WIZARD_WIDTH, WIZARD_HEIGHT, WIZARD_HEALTH)
        self.char = 'W'
        self.range = WIZARD_RANGE
        self.damage = WIZARD_DAMAGE

    def cast(self, army):
        if self.isDestroyed == True:
            return
        for obj in army:
            if obj.isDestroyed == False and self.check_circle_circle_overlap(self.range, self.X+1, self.Y+1, obj.X, obj.Y, obj.X+obj.height, obj.Y+obj.width):
                startx = obj.X
                starty = obj.Y
                for al in army:
                    if al.isDestroyed == False and abs(al.X - startx) <= 1 and abs(al.Y - starty) <= 1:
                        al.health -= self.damage
                        if al.health <= 0:
                            al.isDestroyed = True
                            al.health = 0
                        self.flag = True
                return
        return
