import os
from time import sleep
from colorama import Fore, Back, Style

from constants import *
from player import *
import pickle

# store filename for saving review


c = input("Enter R for review and P for playing game: ")
if c == 'R':
    game = Game()
    game.replay = False
    filename = input("Enter filename: ")
    with open(filename, 'rb') as f:
        fram = pickle.load(f)

    os.system('clear')

    print('CLASH OF CLANS')

    sleep(1)
    l = [2, 3, 4]
    for level in range(0, 3):
        game = Game()
        game.replay = True
        game.king = False
        game.queen = False
        if fram[0] == 0:
            game.king = True
            fram = fram[1:]
        else:
            game.queen = True
            fram = fram[1:]
        game.frame = fram
        # 0 for king and 1 for queen

        game.num_cannon = l[level]
        game.num_wizard = l[level]
        game.prec()
        while game.status:
            print("\033[H\033[J", end="")
            print(game.num_cannon)
            game.play()
        if game.win == 1:
            os.system('clear')
            if level < 2:
                print('You qualify for next level')
                sleep(1)
            else:
                print('You Win!')
                sleep(1)
            fram = fram[(game.nn):]
            FRAMES.clear()
        else:
            print('You Lose!')
            print('You destroyed ' + str(game.num_destroyed) + ' buildings')
            sleep(3)
            FRAMES.clear()
            break
    exit()
elif c == 'P':

    filename = input("Enter filename: ")

    while(os.path.exists(filename)):
        print("File already exists")
        filename = input("Enter filename: ")
    os.system('clear')
    print('CLASH OF CLANS')
    sleep(1)
    l = [2, 3, 4]
    fram = []
    for level in range(0, 3):
        game = Game()
        game.replay = False
        game.king = False
        game.queen = False
        q = input("Do you want to play with king or queen? (K/Q): ")
        if q == 'K':
            game.king = True
            fram.append(0)
        elif q == 'Q':
            game.queen = True
            fram.append(1)
        # 0 for king and 1 for queen

        game.num_cannon = l[level]
        game.num_wizard = l[level]
        game.prec()
        while game.status:
            print("\033[H\033[J", end="")
            print(game.num_cannon)
            game.play()
        if game.win == 1:
            os.system('clear')
            if level < 2:
                print('You qualify for next level')
                sleep(1)
            else:
                print('You Win!')
                sleep(1)
            for i in range(0, len(FRAMES)):
                fram.append(FRAMES[i])
            FRAMES.clear()
        else:
            print('You Lose!')
            print('You destroyed ' + str(game.num_destroyed) + ' buildings')
            sleep(3)
            for i in range(0, len(FRAMES)):
                fram.append(FRAMES[i])
            FRAMES.clear()
            break
    with open(filename, 'wb') as f:
        pickle.dump(fram, f)
else:
    print("Invalid Input")
    exit()
