import sys
import pygame
from pygame.locals import *
import os
import random

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Tile():
	def __init__(self, id, x, y):
		self.Id = id
		self.X = x
		self.Y = y

def createBoard(screen):
    # tilelist = {"": ""}
    # s = 0
    for i in range(tiles):
        for j in range(tiles):
            tile = (screenX//tiles*j, screenY//tiles*i, screenX//tiles, screenY//tiles)
            if i == 0 or j == 0 or i == tiles-1 or j == tiles-1:
                if (i == 0 and j == 0) or (i == tiles-1 and j == 0) or (i == 0 and j == tiles-1) or (i == tiles-1 and j == tiles-1):
                    pygame.draw.rect(screen,(0,255,0),tile)
                else:
                    pygame.draw.rect(screen,(0,200,255),tile, 10)
                # tilelist[s] = Tile(s, j, i)
                # s += 1
                # global tilelist
            else:
                pygame.draw.rect(screen,(0, 0, 0),tile)
    center = pygame.transform.scale(pygame.image.load('BoardCenter.png'), (screenX-(screenX//tiles*2), screenY-(screenY//tiles*2)))
    screen.blit(center, (screenX//tiles,screenY//tiles))

def createList(s, i, j):
	maxtile = tiles-1

	if i == 0 and j == 0:
		tilelist[s] = Tile(s, i, j)
		print("Topleft", s)
		createList(s+1, i, j+1)
	elif i == 0 and j > 0 and j < maxtile:
		tilelist[s] = Tile(s, i, j)
		print("Top", s)
		createList(s+1, i, j+1)
	elif i == 0 and j == maxtile:
		tilelist[s] = Tile(s, i, j)
		print("Topright", s)
		createList(s+1, i+1, j)
	elif i > 0 and i < maxtile and j == maxtile:
		tilelist[s] = Tile(s, i, j)
		print("Right", s)
		createList(s+1, i+1, j)
	elif i == maxtile and j == maxtile:
		tilelist[s] = Tile(s, i, j)
		print("Rightbottom", s)
		createList(s+1, i, j-1)
	elif i == maxtile and j > 0 and j < maxtile:
		tilelist[s] = Tile(s, i, j)
		print("Bottom", s)
		createList(s+1, i, j-1)
	elif i == maxtile and j == 0:
		tilelist[s] = Tile(s, i, j)
		print("Bottomleft", s)
		createList(s+1, i-1, j)
	elif i == 1 and j == 0:
		tilelist[s] = Tile(s, i, j)
	elif i > 0 and i < maxtile and j == 0:
		tilelist[s] = Tile(s, i, j)
		print("Left", s)
		createList(s+1, i-1, j)


def menu(screen):
    pygame.display.flip()
    black = (150, 0, 0)
    screen.fill(black)
    logotexture = pygame.transform.scale(pygame.image.load('logo_super.png'), (screenX, screenY))
    screen.blit(logotexture, (0,0))

    #buttons
    exit_rect = (screenX-screenX / 2 - 250, screenY-screenY /2, 500, 75)    # (x, y, size x, size y)
    start_rect = (screenX-screenX / 2 - 250, screenY-screenY /2-80, 500, 75)
    start_button=screen.fill(black, start_rect)
    exit_button=screen.fill(black, exit_rect)

    #text
    my_font = pygame.font.SysFont("Arial", 70)
    startB_text = my_font.render('START', True, (255,255,255))
    exitB_text = my_font.render("EXIT", True, (255,255,255))   # Text, AA , color
    screen.blit(startB_text,(screenX-screenX / 2 - 115,screenY-screenY /2-80))
    screen.blit(exitB_text, (screenX-screenX / 2 - 80, screenY-screenY /2))     # draws text at 10,10

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if start_button.collidepoint(mpos) and b1==1:
        return
    if exit_button.collidepoint(mpos) and b1==1:
        pygame.quit()
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    menu(screen)

class Pawn():
	def __init__(self, id, sprite, position, x, y):
		self.Id = id
		self.Sprite = sprite
		self.Position = position
		self.X = x
		self.Y = y

def pawnCreate():
	pawns = {"":""}
	for s in range(0, players):
		if s == 0:
			pawnImg = "pawn24bit1.png"
		elif s == 1:
			pawnImg = "pawn24bit2.png"
		elif s == 2:
			pawnImg = "pawn24bit3.png"
		else:
			pawnImg = "pawn24bit4.png"
		pawns[s] = Pawn(s, pygame.transform.scale(pygame.image.load(pawnImg), (screenX//tiles, screenY//tiles)), 1*s, 1*s, 1*s)
		print(pawns[s].Id, pawns[s].Position)
	global pawns

def pawnMove(s, forward):
	pawns[s].Position += forward
	print("Position", pawns[s].Position)
	for i in range(len(tilelist)):
		print("Tile:", tilelist[i].Id, tilelist[i].X, tilelist[i].Y)
		if tilelist[i].Id == pawns[s].Position:
			pawns[s].X = tilelist[i].X*(screenX//tiles)
			pawns[s].Y = tilelist[i].Y*(screenY//tiles)
			break
	print("Tile:", tilelist[i].Id)
	global pawns

def main():
    pygame.init()      # Prepare the pygame module for use
    pygame.display.set_caption('Fightclub')
    
    # for i in range(0,200):
    # 	print(pygame.key.name(i), i)

    try:
        pygame.mixer.music.load('beep.mp3') # muziek
        pygame.mixer.music.play(-1, 0.0)
    except:
        pass

    tilelist = {"": ""}
    tiles = 11
    players = 3
    global tilelist
    global tiles
    global players
    createList(0,0,0)

    screenX, screenY = pygame.display.list_modes()[0]
    if pygame.display.list_modes()[0] == (2880, 1800) or pygame.display.list_modes()[0] == (2560, 1600):
    	HDPI = 2
    	screenX = screenX//HDPI
    	screenY = screenY//HDPI
    screenX -= 100
    screenY -= 100
    screen = pygame.display.set_mode((screenX, screenY))
    global screenX
    global screenY
    global screen
    diceRoll = 0
    pawnCreate()
    menu(screen)

    while True:
        pygame.display.flip()
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
        screen.fill((255, 255, 255))
        createBoard(screen)

        #dice button
        my_font = pygame.font.SysFont("Arial", 70)
        dice_rect = (screenX//tiles, screenY//tiles, 500, 75)
        dice_button=screen.fill((150,0,0), dice_rect)
        dice_text = my_font.render("Roll dice", True, (255,255,255))
        screen.blit(dice_text, (screenX//tiles, screenY//tiles))

        for s in range(players):
        	pygame.event.wait()
        	(b1,b2,b3) = pygame.mouse.get_pressed()
        	mpos = pygame.mouse.get_pos()
	        if dice_button.collidepoint(mpos) and b1 == 1:
	        	diceRoll = random.randint(1,6)
	        	pawnMove(s, 1)
	        	# if pawns[s].Position + diceRoll >= len(tilelist):
	        	# 	diceRoll -= (pawns[s].Position + diceRoll - len(tilelist))
	        	# 	pawnMove(s, diceRoll)
	        	# 	pawns[s].Position = 0
	        	# else:
	        	# 	pawnMove(s, diceRoll)

        for s in range(players):
        	screen.blit(pawns[s].Sprite, (pawns[s].X, pawns[s].Y))

        my_font = pygame.font.SysFont("Arial", 16)
        the_text = my_font.render("Dice: {0}".format(diceRoll), True, (0,0,0))   # Text, AA , color
        screen.blit(the_text, (10, 10))     # draws text at 10,10
        if pygame.key.get_pressed()[27] == 1:
            menu(screen)
        if pygame.key.get_pressed()[113] == 1:
            pygame.quit()
            break 
        my_clock = pygame.time.Clock()
        my_clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()     # Once we leave the loop, close the window.

main()