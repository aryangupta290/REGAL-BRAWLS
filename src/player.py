import time

from defer import return_value
from constants import *
from building import *
import os
from colorama import Fore, Back, Style
from input import *
from troops import *
from spell import *
import math


class Game:
    def __init__(self):
        self.time = time.time()
        self.status = True
        self.GRID = []
        self.timeOut = .1
        self.TownHall = TownHall(TOWN_HALL_X, TOWN_HALL_Y,
                                 TOWN_HALL_WIDTH, TOWN_HALL_HEIGHT, TOWN_HALL_HEALTH)
        wall_X = []
        wall_Y = []
        self.TownHall.get_wall_coords(wall_X, wall_Y)
        self.num_walls = len(wall_X)
        self.Walls = []
        for i in range(self.num_walls):
            self.Walls.append(
                Walls(wall_X[i], wall_Y[i], WALL_WIDTH, WALL_HEIGHT, WALL_HEALTH))
        self.num_huts = 5
        self.Huts = []
        for i in range(0, self.num_huts):
            self.Huts.append(Huts(HUTS_X[i], HUTS_Y[i],
                                  HUTS_WIDTH, HUTS_HEIGHT, HUTS_HEALTH))
        self.cannon = []
        self.num_cannon = 4
        self.num_wizard = 4
        self.wizard = []
        self.is_king = False
        self.is_queen = False
        self.Barbarian = []
        self.cur_barb = 0
        self.barb_lim = BARBARIAN_LIMIT
        self.Archer = []
        self.cur_archer = 0
        self.archer_lim = ARCHER_LIMIT
        self.Loon = []
        self.cur_loon = 0
        self.loon_lim = LOON_LIMIT
        self.Heal = Spells()
        self.Rage = Spells()
        self.win = 0
        self.num_destroyed = 0
        self.fixed_Walls = []
        Buildings.outer_wall_coords(Buildings, self.fixed_Walls)
        self.nn = 0

    def prec(self):
        for i in range(self.num_cannon):
            self.cannon.append(Cannon(CANNON_X[i], CANNON_Y[i],
                                      CANNON_WIDTH, CANNON_HEIGHT, CANNON_HEALTH))
        for i in range(self.num_wizard):
            self.wizard.append(Wizard(WIZARD_X[i], WIZARD_Y[i],
                                      WIZARD_WIDTH, WIZARD_HEIGHT, WIZARD_HEALTH))

    def show(self):
        self.GRID = [[' ']*COLS for rows in range(ROWS)]
        for i in range(ROWS):
            self.GRID[i].append('\n')
        for i in range(len(self.fixed_Walls)):
            self.fixed_Walls[i].display(self.GRID)
        Buildings.display(self.TownHall, self.GRID)
        for i in range(self.num_walls):
            Walls.display(self.Walls[i], self.GRID)
        for hut in self.Huts:
            Buildings.display(hut, self.GRID)
        for c in self.cannon:
            Cannon.display(c, self.GRID)
        for w in self.wizard:
            Wizard.display(w, self.GRID)

        for barbarian in self.Barbarian:
            Barbarian.set_pixel(barbarian, 0)
            Barbarian.display(barbarian, self.GRID)
        for archer in self.Archer:
            Archer.set_pixel(archer, 1)
            Archer.display(archer, self.GRID)
        for loon in self.Loon:
            Loons.set_pixel(loon, 2)
            Loons.display(loon, self.GRID)
        if self.king == True and self.is_king == True:
            King.display(self.King, self.GRID)
        if self.queen == True and self.is_queen == True:
            Queen.display(self.Queen, self.GRID)

    def print_current_grid(self):
        for row in self.GRID:
            for col in row:
                print(col, end="")

        if self.king == True and self.is_king == True:
            str = ""
            for i in range(math.ceil(self.King.health)):
                str += "█"
            print("\n" + "Health: " + str)
        if self.queen == True and self.is_queen == True:
            str = ""
            for i in range(math.ceil(self.Queen.health)):
                str += "█"
            print("\n" + "Health: " + str)

    def is_win(self):
        if self.TownHall.isDestroyed == False:
            return False
        for hut in self.Huts:
            if hut.isDestroyed == False:
                return False
        for i in self.cannon:
            if i.isDestroyed == False:
                return False
        for i in self.wizard:
            if i.isDestroyed == False:
                return False
        return True

    def is_lose(self):
        if self.cur_barb < self.barb_lim or self.cur_archer < self.archer_lim or self.cur_loon < self.loon_lim:
            return False
        if self.king == True and self.is_king == False:
            return False
        if self.queen == True and self.is_queen == False:
            return False
        if self.king == True and self.King.isDestroyed == False:
            return False
        if self.queen == True and self.Queen.isDestroyed == False:
            return False
        for barb in self.Barbarian:
            if barb.isDestroyed == False:
                return False
        for archer in self.Archer:
            if archer.isDestroyed == False:
                return False
        for loon in self.Loon:
            if loon.isDestroyed == False:
                return False
        return True

    def barb_attack(self, obj):
        building = []
        building.append(self.TownHall)
        for j in range(self.num_walls):
            building.append(self.Walls[j])
        for j in range(self.num_huts):
            building.append(self.Huts[j])
        for j in self.wizard:
            building.append(j)
        for j in self.cannon:
            building.append(j)
        for j in range(0, obj.repeat):
            Barbarian.attack(obj, building)

    def archer_attack(self, obj):
        building = []
        building.append(self.TownHall)
        for j in self.wizard:
            building.append(j)
        for j in self.cannon:
            building.append(j)
        for j in range(self.num_walls):
            building.append(self.Walls[j])
        for j in range(self.num_huts):
            building.append(self.Huts[j])

        for j in range(0, obj.repeat):
            Archer.attack(obj, building)

    def loon_attack(self, obj):
        defensive = []
        non_defensive = []
        non_defensive.append(self.TownHall)
        for j in self.wizard:
            defensive.append(j)
        for j in self.cannon:
            defensive.append(j)
        for j in range(self.num_huts):
            non_defensive.append(self.Huts[j])
        for j in range(0, obj.repeat):
            Loons.attack(obj, defensive, non_defensive)

    def play(self):
        os.system('clear')

        if self.is_win() == True:
            self.status = False
            self.win = 1
            return

        if self.is_lose() == True:
            self.status = False
            self.win = 2
            if self.TownHall.isDestroyed == True:
                self.num_destroyed += 1
            for hut in self.Huts:
                if hut.isDestroyed == True:
                    self.num_destroyed += 1
            for i in range(self.num_cannon):
                if self.cannon[i].isDestroyed == True:
                    self.num_destroyed += 1
            for i in range(self.num_wizard):
                if self.wizard[i].isDestroyed == True:
                    self.num_destroyed += 1
            return

        army = []
        if self.is_king == True:
            army.append(self.King)
        if self.is_queen == True:
            army.append(self.Queen)
        for i in range(0, self.cur_barb):
            army.append(self.Barbarian[i])
        for archer in self.Archer:
            army.append(archer)

        for i in range(self.num_cannon):
            Cannon.shoot(self.cannon[i], army)
        for i in self.Loon:
            army.append(i)
        for i in range(self.num_wizard):
            Wizard.cast(self.wizard[i], army)

        for i in range(0, self.cur_barb):
            self.barb_attack(self.Barbarian[i])

        for i in range(0, self.cur_archer):
            self.archer_attack(self.Archer[i])

        for i in range(0, self.cur_loon):
            self.loon_attack(self.Loon[i])

        Game.show(self)
        self.print_current_grid()
        if self.replay == True:
            key = self.frame[self.nn]
            time.sleep(.1)

        else:
            inp = Input()
            key = inp.get_parsed_input(self.timeOut)
            FRAMES.append(key)
        objects = []
        objects.append(self.TownHall)
        for i in range(self.num_walls):
            objects.append(self.Walls[i])
        for hut in self.Huts:
            objects.append(hut)
        for i in range(self.num_cannon):
            objects.append(self.cannon[i])
        for i in range(self.num_wizard):
            objects.append(self.wizard[i])
        if self.queen == True and self.is_queen == True:
            self.Queen.check(objects, self.nn)

        army.clear()
        if self.king == True and self.is_king == True:
            army.append(self.King)
        if self.queen == True and self.is_queen == True:
            army.append(self.Queen)
        for i in range(0, self.cur_barb):
            army.append(self.Barbarian[i])
        for i in range(0, self.cur_archer):
            army.append(self.Archer[i])
        for i in range(0, self.cur_loon):
            army.append(self.Loon[i])
        if key == 'quit':
            self.status = False
            return
        if key == 'up':
            if self.king == True:
                if self.is_king == True:
                    for i in range(0, self.King.repeat):
                        Troops.move(self.King, -1, 0, objects)
            else:
                if self.is_queen == True:
                    for i in range(0, self.Queen.repeat):
                        Troops.move(self.Queen, -1, 0, objects)

        if key == 'down':
            if self.king == True:
                if self.is_king == True:
                    for i in range(0, self.King.repeat):
                        Troops.move(self.King, 1, 0, objects)
            else:
                if self.is_queen == True:
                    for i in range(0, self.Queen.repeat):
                        Troops.move(self.Queen, 1, 0, objects)

        if key == 'left':
            if self.king == True:
                if self.is_king == True:
                    for i in range(0, self.King.repeat):
                        Troops.move(self.King, 0, -1, objects)
            else:
                if self.is_queen == True:
                    for i in range(0, self.Queen.repeat):
                        Troops.move(self.Queen, 0, -1,  objects)

        if key == 'right':
            if self.king == True:
                if self.is_king == True:
                    for i in range(0, self.King.repeat):
                        Troops.move(self.King,  0, 1, objects)
            else:
                if self.is_queen == True:
                    for i in range(0, self.Queen.repeat):
                        Troops.move(self.Queen,  0, 1, objects)

        if key == 'space':

            if self.is_king == True:
                for i in range(0, self.King.repeat):
                    King.attack(self.King, objects, 0, 2)
            if self.is_queen == True:
                for i in range(0, self.Queen.repeat):
                    Queen.attack(self.Queen, objects)
        if key == 'e':
            if self.is_king == True:
                King.special_attack(self.King, objects)
        if key == 's1' and self.cur_barb < self.barb_lim:
            self.Barbarian.append(Barbarian(
                SPAWNING_X[0], SPAWNING_Y[0], BARBARIAN_WIDTH, BARBARIAN_HEIGHT, BARBARIAN_HEALTH, BARBARIAN_DAMAGE))
            self.cur_barb += 1
        if key == 's2' and self.cur_barb < self.barb_lim:
            self.Barbarian.append(Barbarian(
                SPAWNING_X[1], SPAWNING_Y[1], BARBARIAN_WIDTH, BARBARIAN_HEIGHT, BARBARIAN_HEALTH, BARBARIAN_DAMAGE))
            self.cur_barb += 1
        if key == 's3' and self.cur_barb < self.barb_lim:
            self.Barbarian.append(Barbarian(
                SPAWNING_X[2], SPAWNING_Y[2], BARBARIAN_WIDTH, BARBARIAN_HEIGHT, BARBARIAN_HEALTH, BARBARIAN_DAMAGE))
            self.cur_barb += 1
        if key == 'a1' and self.cur_archer < self.archer_lim:
            self.Archer.append(Archer(
                SPAWNING_X[0], SPAWNING_Y[0], ARCHER_WIDTH, ARCHER_HEIGHT, ARCHER_HEALTH, ARCHER_DAMAGE))
            self.cur_archer += 1
        if key == 'a2' and self.cur_archer < self.archer_lim:
            self.Archer.append(Archer(
                SPAWNING_X[1], SPAWNING_Y[1], ARCHER_WIDTH, ARCHER_HEIGHT, ARCHER_HEALTH, ARCHER_DAMAGE))
            self.cur_archer += 1
        if key == 'a3' and self.cur_archer < self.archer_lim:
            self.Archer.append(Archer(
                SPAWNING_X[2], SPAWNING_Y[2], ARCHER_WIDTH, ARCHER_HEIGHT, ARCHER_HEALTH, ARCHER_DAMAGE))
            self.cur_archer += 1
        if key == 'l1' and self.cur_loon < self.loon_lim:
            self.Loon.append(Loons(
                SPAWNING_X[0], SPAWNING_Y[0], LOON_WIDTH, LOON_HEIGHT, LOON_HEALTH, LOON_DAMAGE))
            self.cur_loon += 1
        if key == 'l2' and self.cur_loon < self.loon_lim:
            self.Loon.append(Loons(
                SPAWNING_X[1], SPAWNING_Y[1], LOON_WIDTH, LOON_HEIGHT, LOON_HEALTH, LOON_DAMAGE))
            self.cur_loon += 1
        if key == 'l3' and self.cur_loon < self.loon_lim:
            self.Loon.append(Loons(
                SPAWNING_X[2], SPAWNING_Y[2], LOON_WIDTH, LOON_HEIGHT, LOON_HEALTH, LOON_DAMAGE))
            self.cur_loon += 1
        if key == 'k1' and self.king == True and self.is_king == False:
            self.King = King(SPAWNING_X[0], SPAWNING_Y[0], KING_WIDTH,
                             KING_HEIGHT, KING_HEALTH, KING_DAMAGE)
            self.is_king = True
        if key == 'k2' and self.king == True and self.is_king == False:
            self.King = King(SPAWNING_X[1], SPAWNING_Y[1], KING_WIDTH,
                             KING_HEIGHT, KING_HEALTH, KING_DAMAGE)
            self.is_king = True
        if key == 'k3' and self.king == True and self.is_king == False:
            self.King = King(SPAWNING_X[2], SPAWNING_Y[2], KING_WIDTH,
                             KING_HEIGHT, KING_HEALTH, KING_DAMAGE)
            self.is_king = True
        if key == 'k1' and self.queen == True and self.is_queen == False:
            self.Queen = Queen(SPAWNING_X[0], SPAWNING_Y[0], QUEEN_WIDTH,
                               QUEEN_HEIGHT, QUEEN_HEALTH, QUEEN_DAMAGE)
            self.is_queen = True
        if key == 'k2' and self.queen == True and self.is_queen == False:
            self.Queen = Queen(SPAWNING_X[1], SPAWNING_Y[1], QUEEN_WIDTH,
                               QUEEN_HEIGHT, QUEEN_HEALTH, QUEEN_DAMAGE)
            self.is_queen = True
        if key == 'k3' and self.queen == True and self.is_queen == False:
            self.Queen = Queen(SPAWNING_X[2], SPAWNING_Y[2], QUEEN_WIDTH,
                               QUEEN_HEIGHT, QUEEN_HEALTH, QUEEN_DAMAGE)
            self.is_queen = True
        if key == 'heal' and self.Heal.cur < self.Heal.max_lim:
            self.Heal.power_up(army, 3/2, 1)
            self.Heal.increase()
        if key == 'rage' and self.Rage.cur < self.Rage.max_lim:
            self.Rage.power_up(army, 1, 2)
            self.Rage.increase()
        if key == 'queen' and self.queen == True and self.is_queen == True:
            self.Queen.special_attack(self.nn)
        self.nn = 1 + self.nn
