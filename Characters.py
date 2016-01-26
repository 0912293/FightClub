import sys
import pygame
from pygame.locals import *
import os
import random

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Character():
    def __init__(self, id, name, attacks, removestamina):
        self.Id = id
        self.Name = name[id]
        self.Attacks = attacks[id]
        self.Removestamina = removestamina[id]

name = {0:"Rocky Belboa", 1:"Manny Pecquiao", 2:"Mike Tysen", 3:"Badr Heri"}

attacks = {0: {1:-10, 2:-20, 3:-30},
           1: {1:-10, 2:-20, 3:-30},
           2: {1:-10, 2:-20, 3:-30},
           3: {1:-10, 2:-20, 3:-30}}

removestamina = {0: {1:-3, 2:-6, 3:-9},
                 1: {1:-3, 2:-6, 3:-9},
                 2: {1:-3, 2:-6, 3:-9},
                 3: {1:-3, 2:-6, 3:-9}}

