import sys
import pygame
from pygame.locals import *
import os
import random

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Cards():
    def __init__(self, id):
        self.Id = id
        self.Name = cardDict[id]
        self.Damage = cardDamage[id]
        self.Sprite = os.path.join("img", "sf"+id+".png")

cardDict = {0:"Terry Crews", 1:"Jason Statham", 2:"Wesley Sniper", 3:"Jet Ri", 4:"Steve Seagal",
                5:"Super Merio", 6:"Vin Dieser", 7:"Chack Norris", 8:"The Roch", 9:"Ernold Schwarzenegger",
                10:"Pariz Hilten", 11:"Jackie Chen", 12:"Steve Urkel", 13:"John Cena", 14:"James Bend",
                15:"Dexter", 16:"Agua Man", 17:"Bruce Hee"}
cardDamage = {0:16, 1:18, 2:13, 3:20, 4:16, 5:15, 6:13, 7:32, 8:24, 9:26,
              10:6, 11:9, 12:7, 13:26, 14:28, 15:13, 16:7, 17:29}
