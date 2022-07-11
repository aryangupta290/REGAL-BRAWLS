from constants import *
from colorama import Fore, Back, Style


class Troops():
    def __init__(self, startX, startY, width, height, health, damage):
        self.isDestroyed = False
        self.X = startX
        self.Y = startY
        self.width = width
        self.height = height
        self.health = health
        self.totalHealth = health
        self.damage = damage
        self.repeat = 1

    def display(self, GRID):
        for i in range(self.height):
            for j in range(self.width):
                GRID[self.X+i][self.Y+j] = self.pixel + \
                    self.char + Style.RESET_ALL

    def out_of_bound(self, x, y, w, h):
        for i in range(x, x+h):
            for j in range(y, y+w):
                if i < 1 or i >= ROWS-1 or j < 1 or j >= COLS-1:
                    return True
        return False

    def check_circle_rectangle_overlap(self, R, Xc, Yc, X1, Y1, X2, Y2):
        Xn = max(X1, min(Xc, X2))
        Yn = max(Y1, min(Yc, Y2))
        Dx = Xn - Xc
        Dy = Yn - Yc
        return (Dx**2 + Dy**2) <= R**2

    def move(self, x, y, objects):
        if self.isDestroyed == True:
            return False
        for obj in objects:
            if obj.isDestroyed == True:
                continue
            for i in range(0, self.height):
                for j in range(0, self.width):
                    if self.collide(obj, i+x, j+y):
                        return False
        if self.out_of_bound(self.X + x, self.Y+y, self.width, self.height):
            return False
        self.X += x
        self.Y += y
        if x == -1:
            self.which = 0
        elif x == 1:
            self.which = 1
        elif y == -1:
            self.which = 2
        else:
            self.which = 3
        return True

    def collide(self, obj, x, y):
        if obj.isDestroyed == True:
            return False
        for i in range(obj.X, obj.X + obj.height):
            for j in range(obj.Y, obj.Y + obj.width):
                if i == self.X + x and j == self.Y + y:
                    return True
        return False

    def attack(self, objects, x, y):
        if self.isDestroyed == True:
            return
        for obj in objects:
            if obj.isDestroyed == True:
                continue
            is_inside = False
            for i in range(obj.X, obj.X + obj.height):
                for j in range(obj.Y, obj.Y + obj.width):
                    if i == self.X + x and j == self.Y+y:
                        is_inside = True
                        break
                if is_inside == True:
                    break
            if is_inside == True:
                obj.health -= self.damage
                if obj.health <= 0:
                    obj.isDestroyed = True
                    obj.health = 0

    def set_pixel(self, which):
        if which == 0:
            self.char = 'B'
        elif which == 1:
            self.char = 'A'
        else:
            self.char = 'L'
        h = self.health/self.totalHealth
        h *= 100
        if h > 50:
            self.pixel = Fore.RED
        else:
            self.pixel = Fore.RED + Style.DIM

    def attack_and_move(self, objects):
        min_dist = 1000000
        min_obj = None
        min_x = 0
        min_y = 0
        for obj in objects:
            if obj.isDestroyed == True or obj.width == 1:
                continue
            d = 1000000
            x = 0
            y = 0
            for i in range(obj.X, obj.X + obj.height):
                for j in range(obj.Y, obj.Y + obj.width):
                    if d > abs(i-self.X) + abs(j-self.Y):
                        d = abs(i-self.X) + abs(j-self.Y)
                        x = i
                        y = j
            if min_dist > d:
                min_dist = d
                min_obj = obj
                min_x = x
                min_y = y
        if min_obj is None:
            return
        move_in_x = 0
        move_in_y = 0

        if min_x > self.X:
            move_in_x = 1
        elif min_x < self.X:
            move_in_x = -1
        if min_y > self.Y:
            move_in_y = 1
        elif min_y < self.Y:
            move_in_y = -1
        if self.flip == 0:
            if self.move(move_in_x, 0, objects) == True:
                self.flip = 1
            elif move_in_x != 0:
                for obj in objects:
                    if obj.isDestroyed == True:
                        continue
                    if self.collide(obj, move_in_x, 0):
                        obj.health -= self.damage
                        if obj.health <= 0:
                            obj.isDestroyed = True
                            obj.health = 0
                        return
            else:
                for obj in objects:
                    if obj.isDestroyed == True:
                        continue
                    if self.collide(obj, 0, move_in_y):
                        obj.health -= self.damage
                        if obj.health <= 0:
                            obj.isDestroyed = True
                            obj.health = 0
                        return

                self.move(0, move_in_y, objects)
                self.flip = 1 - self.flip
        else:
            if self.move(0, move_in_y,  objects) == True:
                self.flip = 0
            elif move_in_y != 0:
                for obj in objects:
                    if obj.isDestroyed == True:
                        continue
                    if self.collide(obj, 0, move_in_y):
                        obj.health -= self.damage
                        if obj.health <= 0:
                            obj.isDestroyed = True
                            obj.health = 0
                        return
            else:
                for obj in objects:
                    if obj.isDestroyed == True:
                        continue
                    if self.collide(obj, move_in_x, 0):
                        obj.health -= self.damage
                        if obj.health <= 0:
                            obj.isDestroyed = True
                            obj.health = 0
                        return

                self.move(move_in_x, 0, objects)
                self.flip = 1 - self.flip


class King(Troops):
    def __init__(self, KING_X, KING_Y, KING_WIDTH, KING_HEIGHT, KING_HEALTH, KING_DAMAGE):
        super().__init__(KING_X, KING_Y, KING_WIDTH, KING_HEIGHT, KING_HEALTH, KING_DAMAGE)
        self.char = 'K'
        self.pixel = Back.CYAN
        self.which = 0

    def special_attack(self, objects):
        if self.isDestroyed == True:
            return
        for obj in objects:
            if obj.isDestroyed == True:
                continue
            if self.check_circle_rectangle_overlap(KING_RADIUS, self.X+1, self.Y+1, obj.X, obj.Y, obj.X+obj.width, obj.Y+obj.height):
                obj.health -= self.damage
                if obj.health <= 0:
                    obj.isDestroyed = True
                    obj.health = 0


class Queen(Troops):
    def __init__(self, QUEEN_X, QUEEN_Y, QUEEN_WIDTH, QUEEN_HEIGHT, QUEEN_HEALTH, QUEEN_DAMAGE):
        super().__init__(QUEEN_X, QUEEN_Y, QUEEN_WIDTH,
                         QUEEN_HEIGHT, QUEEN_HEALTH, QUEEN_DAMAGE)
        self.char = 'Q'
        self.pixel = Back.CYAN
        self.which = 0
        self.later_attack = {}

    def attack(self, objects):
        if self.isDestroyed == True:
            return
        for obj in objects:
            if obj.isDestroyed == True:
                continue
            startx = self.X
            starty = self.Y
            if self.which == 0:  # up
                startx -= 8
            elif self.which == 1:  # down
                startx += 8
            elif self.which == 2:  # left
                starty -= 8
            elif self.which == 3:  # right
                starty += 8
            for i in range(obj.X, obj.X + obj.height):
                for j in range(obj.Y, obj.Y + obj.width):
                    if abs(startx-i) <= 2 and abs(starty-j) <= 2:
                        obj.health -= self.damage
                        if obj.health <= 0:
                            obj.isDestroyed = True
                            obj.health = 0

    def special_attack(self, nn):
        if self.isDestroyed == True:
            return
        x = self.X
        y = self.Y
        if self.which == 0:
            x -= 16
        elif self.which == 1:
            x += 16
        elif self.which == 2:
            y -= 16
        elif self.which == 3:
            y += 16
        self.later_attack[nn+10] = (x, y)

    def check(self, objects, nn):
        if self.isDestroyed == True:
            return
        if nn in self.later_attack:
            x = self.later_attack[nn][0]
            y = self.later_attack[nn][1]
            for obj in objects:
                if obj.isDestroyed == True:
                    continue
                if abs(obj.X-x) <= 4 and abs(obj.Y-y) <= 4:
                    obj.health -= self.damage
                    if obj.health <= 0:
                        obj.isDestroyed = True
                        obj.health = 0
            del self.later_attack[nn]


class Barbarian(Troops):
    def __init__(self, BARBARIAN_X, BARBARIAN_Y, BARBARIAN_WIDTH, BARBARIAN_HEIGHT, BARBARIAN_HEALTH, BARBARIAN_DAMAGE):
        super().__init__(BARBARIAN_X, BARBARIAN_Y, BARBARIAN_WIDTH,
                         BARBARIAN_HEIGHT, BARBARIAN_HEALTH, BARBARIAN_DAMAGE)

        self.flip = 0

    def attack(self, objects):
        if self.isDestroyed == True:
            return
        self.attack_and_move(objects)


class Archer(Troops):
    def __init__(self, ARCHER_X, ARCHER_Y, ARCHER_WIDTH, ARCHER_HEIGHT, ARCHER_HEALTH, ARCHER_DAMAGE):
        super().__init__(ARCHER_X, ARCHER_Y, ARCHER_WIDTH,
                         ARCHER_HEIGHT, ARCHER_HEALTH, ARCHER_DAMAGE)

        self.flip = 0
        self.repeat = 2
        self.range = ARCHER_RANGE
        self.damage = self.damage/2

    def attack(self, objects):
        if self.isDestroyed == True:
            return
        for obj in objects:
            if obj.isDestroyed == False and obj.width > 1 and self.check_circle_rectangle_overlap(self.range, self.X+1, self.Y+1, obj.X, obj.Y, obj.X+obj.height, obj.Y+obj.width):
                obj.health -= self.damage
                if obj.health <= 0:
                    obj.isDestroyed = True
                    obj.health = 0
                return
        self.attack_and_move(objects)


class Loons(Troops):
    def __init__(self, LOONS_X, LOONS_Y, LOONS_WIDTH, LOONS_HEIGHT, LOONS_HEALTH, LOONS_DAMAGE):
        super().__init__(LOONS_X, LOONS_Y, LOONS_WIDTH,
                         LOONS_HEIGHT, LOONS_HEALTH, LOONS_DAMAGE)

        self.flip = 0
        self.repeat = 2

    def attack(self, defensive, non_defensive):
        if self.isDestroyed == True:
            return
        for obj in defensive:
            if obj.isDestroyed == True:
                continue
            for i in range(0, self.height):
                for j in range(0, self.width):
                    if self.collide(obj, i, j):
                        obj.health -= self.damage
                        if obj.health <= 0:
                            obj.isDestroyed = True
                            obj.health = 0
                        return
        min_dist = 1000000
        min_obj = None
        min_x = 0
        min_y = 0
        for obj in defensive:
            if obj.isDestroyed == True:
                continue
            d = 1000000
            x = 0
            y = 0
            for i in range(obj.X, obj.X + obj.height):
                for j in range(obj.Y, obj.Y + obj.width):
                    if d > abs(i-self.X) + abs(j-self.Y):
                        d = abs(i-self.X) + abs(j-self.Y)
                        x = i
                        y = j
            if min_dist > d:
                min_dist = d
                min_obj = obj
                min_x = x
                min_y = y
        if min_obj != None:
            move_in_x = 0
            move_in_y = 0

            if min_x > self.X:
                move_in_x = 1
            elif min_x < self.X:
                move_in_x = -1
            if min_y > self.Y:
                move_in_y = 1
            elif min_y < self.Y:
                move_in_y = -1
            if self.flip == 0:
                if move_in_x != 0:
                    self.X += move_in_x
                    self.flip = 1
                else:
                    self.Y += move_in_y
                    self.flip = 1 - self.flip
            else:
                if move_in_y != 0:
                    self.Y += move_in_y
                    self.flip = 0
                else:
                    self.X += move_in_x
                    self.flip = 1 - self.flip
            return

        for obj in non_defensive:
            if obj.isDestroyed == True:
                continue
            for i in range(0, self.height):
                for j in range(0, self.width):
                    if self.collide(obj, i, j):
                        obj.health -= self.damage
                        if obj.health <= 0:
                            obj.isDestroyed = True
                            obj.health = 0
                        return
        min_dist = 1000000
        min_obj = None
        min_x = 0
        min_y = 0
        for obj in non_defensive:
            if obj.isDestroyed == True:
                continue
            d = 1000000
            x = 0
            y = 0
            for i in range(obj.X, obj.X + obj.height):
                for j in range(obj.Y, obj.Y + obj.width):
                    if d > abs(i-self.X) + abs(j-self.Y):
                        d = abs(i-self.X) + abs(j-self.Y)
                        x = i
                        y = j
            if min_dist > d:
                min_dist = d
                min_obj = obj
                min_x = x
                min_y = y
        if min_obj != None:
            move_in_x = 0
            move_in_y = 0

            if min_x > self.X:
                move_in_x = 1
            elif min_x < self.X:
                move_in_x = -1
            if min_y > self.Y:
                move_in_y = 1
            elif min_y < self.Y:
                move_in_y = -1
            if self.flip == 0:
                if move_in_x != 0:
                    self.X += move_in_x
                    self.flip = 1
                else:
                    self.Y += move_in_y
                    self.flip = 1 - self.flip
            else:
                if move_in_y != 0:
                    self.Y += move_in_y
                    self.flip = 0
                else:
                    self.X += move_in_x
                    self.flip = 1 - self.flip
        return
