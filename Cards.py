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

cardNameDict = {0:"Terry Crews", 1:"Jason Statham", 2:"Wesley Sniper", 3:"Jet Ri", 4:"Steve Seagal", 5:"Super Merio", 6:"Vin Dieser", 7:"Chack Norris", 8:"The Roch", 9:"Ernold Schwarzenegger", 10:"Pariz Hilten", 11:"Jackie Chen", 12:"Steve Urkel", 13:"John Cena", 14:"James Bend", 15:"Dexter", 16:"Agua Man", 17:"Bruce Hee"}
cardDamage = {0:16, 1:20, 2:13, 3:19, 4:16, 5:18, 6:23, 7:26, 8:18, 9:18, 10:11, 11:14, 12:10, 13:11, 14:18, 15:10, 16:11, 17:14}
