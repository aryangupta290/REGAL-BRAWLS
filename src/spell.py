from constants import *
from colorama import Fore, Back, Style
import time


class Spells():
    def __init__(self):
        self.max_lim = 7
        self.cur = 0
        self.time = time.time()

    def increase(self):
        self.cur = self.cur + 1

    def power_up(self, objects, heal, rage):
        for obj in objects:
            if obj.isDestroyed == False:
                h = obj.totalHealth
                val = min(h, (heal*obj.health))
                obj.health = val
        for obj in objects:
            if obj.isDestroyed == False:
                k = obj.damage
                k = k * rage
                obj.repeat = obj.repeat * rage
