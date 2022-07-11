
import os
import json
from colorama import Fore, Back
import sys
import termios
import tty
import signal
from time import sleep
from re import sub
from random import choice


class Cursor:
    def __init__(self):
        self.__hide_string = "\x1b[?25l"
        self.__show_string = "\x1b[?25h"

    def hide(self):
        print(self.__hide_string)

    def show(self):
        print(self.__show_string)


class Input:
    def _get_key_raw(self):
        fd = sys.stdin.fileno()
        self.old_config = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.buffer.raw.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, self.old_config)
        return ch

    def _timeout_handler(self, signum, frame):
        raise TimeoutError

    def get_parsed_input(self, timeout):
        signal.signal(signal.SIGALRM, self._timeout_handler)
        signal.setitimer(signal.ITIMER_REAL, timeout)
        try:
            ip = self._get_key_raw()
            signal.alarm(0)
            if ip == b'\x03':
                key = 'quit'
            elif ip in [b'a', b'A']:
                key = 'left'
            elif ip in [b'd', b'D']:
                key = 'right'
            elif ip in [b's', b'S']:
                key = 'down'
            elif ip in [b'w', b'W']:
                key = 'up'
            elif ip == b' ':
                key = 'space'
            elif ip in [b'e', b'E']:
                key = 'e'
            elif ip in [b'1']:
                key = 's1'
            elif ip in [b'2']:
                key = 's2'
            elif ip in [b'3']:
                key = 's3'
            elif ip in [b'z']:
                key = 'a1'
            elif ip in [b'x']:
                key = 'a2'
            elif ip in [b'c']:
                key = 'a3'
            elif ip in [b'v']:
                key = 'l1'
            elif ip in [b'b']:
                key = 'l2'
            elif ip in [b'n']:
                key = 'l3'
            elif ip in [b'4']:
                key = 'k1'
            elif ip in [b'5']:
                key = 'k2'
            elif ip in [b'6']:
                key = 'k3'
            elif ip in [b'7']:
                key = 'heal'
            elif ip in [b'8']:
                key = 'rage'
            elif ip in [b'9']:
                key = 'queen'
            else:
                key = 'none'
            sleep(timeout)
            return key
        except TimeoutError:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
            return None
