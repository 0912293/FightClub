import sys
import pygame
from pygame.locals import *
import os
import random

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Cards():
    def __init__(self, id, name):
        self.Id = id
        self.Name = cardDict[id]
        self.Sprite = os.path.join("img", "sf"+id+".png")

cardDict = {0:"First", 1:"Second"}