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
        createList(s+1, i, j+1)
    elif i == 0 and j > 0 and j < maxtile:
        tilelist[s] = Tile(s, i, j)
        createList(s+1, i, j+1)
    elif i == 0 and j == maxtile:
        tilelist[s] = Tile(s, i, j)
        createList(s+1, i+1, j)
    elif i > 0 and i < maxtile and j == maxtile:
        tilelist[s] = Tile(s, i, j)
        createList(s+1, i+1, j)
    elif i == maxtile and j == maxtile:
        tilelist[s] = Tile(s, i, j)
        createList(s+1, i, j-1)
    elif i == maxtile and j > 0 and j < maxtile:
        tilelist[s] = Tile(s, i, j)
        createList(s+1, i, j-1)
    elif i == maxtile and j == 0:
        tilelist[s] = Tile(s, i, j)
        createList(s+1, i-1, j)
    elif i == 1 and j == 0:
        tilelist[s] = Tile(s, i, j)
    elif i > 0 and i < maxtile and j == 0:
        tilelist[s] = Tile(s, i, j)
        createList(s+1, i-1, j)

def menu():
    pygame.display.flip()
    black = (0, 0, 0)
    red = (150, 0, 0)
    screen.fill(red)
    logotexture = pygame.transform.scale(pygame.image.load('logo_super.png'), (screenX, screenY))
    screen.blit(logotexture, (0,0))

    #buttons (x, y, size x, size y)
    start_rect = (0, 50, screenX, 75)
    instruct_rect = (0, 150, screenX, 75)
    exit_rect = (0, 250, screenX, 75) 

    start_button=screen.fill(black, start_rect)
    instruct_button=screen.fill(black, instruct_rect)
    exit_button=screen.fill(black, exit_rect)

    #text Text, AA , color
    my_font = pygame.font.SysFont("Arial", 70)
    startB_text = my_font.render('START', True, (255,255,255))
    instructB_text = my_font.render('INSTRUCTIONS', True, (255,255,255))
    exitB_text = my_font.render("EXIT", True, (255,255,255))
    
    #draw text
    screen.blit(startB_text,(screenX//2-(len("START")*20), 50))
    screen.blit(instructB_text,(screenX//2-(len("INSTRUCTIONS")*20), 150))
    screen.blit(exitB_text, (screenX//2-(len("EXIT")*20), 250))

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if start_button.collidepoint(mpos) and b1==1:
        return
    if instruct_button.collidepoint(mpos) & b1==1:
        instructions()
    if exit_button.collidepoint(mpos) and b1==1:
        pygame.quit()
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    menu()

def instructions():
    pygame.display.flip()
    black = (0, 0, 0)
    red = (150, 0, 0)
    screen.fill(red)
    logotexture = pygame.transform.scale(pygame.image.load('logo_super.png'), (screenX, screenY))
    screen.blit(logotexture, (0,0))

    background_rect = (0, 50, screenX, screenY-200)
    background=screen.fill(black, background_rect)
    return_rect = (0, screenY-100, screenX, 75)
    return_button=screen.fill(black, return_rect)
    #text Text, AA , color
    font = pygame.font.SysFont("Arial", 40)
    background_text1 = font.render("1.Press the escape key to open the menu", True, (255,255,255))
    background_text2 = font.render("2.To move your pawn press the 'Roll dice' button", True, (255,255,255))
    font = pygame.font.SysFont("Arial", 70)
    return_text = font.render('RETURN', True, (255,255,255))
    #draw text
    screen.blit(background_text1,(screenX//2-(len("1.Press the escape key to open the menu")*8), 150))
    screen.blit(background_text2,(screenX//2-(len("2.To move your pawn press the 'Roll dice' button")*8), 250))
    screen.blit(return_text, (screenX//2-(len("RETURN")*20), screenY-100))

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if return_button.collidepoint(mpos) and b1==1:
        return
    if pygame.key.get_pressed()[27] == 1:
        return
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    instructions()

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
    global pawns

def pawnMove(s, forward):
    if pawns[s].Position + forward > len(tilelist)-1:
        remainder = pawns[s].Position + forward - len(tilelist)-1
        pawns[s].Position = remainder
    pawns[s].Position += forward
    for i in range(len(tilelist)-1):
        if tilelist[i].Id == pawns[s].Position:
            pawns[s].X = tilelist[i].X*(screenX//tiles)
            pawns[s].Y = tilelist[i].Y*(screenY//tiles)
            break

def main():
    pygame.init()      # Prepare the pygame module for use
    pygame.display.set_caption('Fightclub')
    
    # for i in range(0,200):
    #   print(pygame.key.name(i), i)

    try:
        pygame.mixer.music.load('beep.mp3') # Attempts to play music
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
    menu()

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
                #   diceRoll -= (pawns[s].Position + diceRoll - len(tilelist))
                #   pawnMove(s, diceRoll)
                #   pawns[s].Position = 0
                # else:
                #   pawnMove(s, diceRoll)

        for s in range(players):
            screen.blit(pawns[s].Sprite, (pawns[s].X, pawns[s].Y))

        my_font = pygame.font.SysFont("Arial", 16)
        the_text = my_font.render("Dice: {0}".format(diceRoll), True, (0,0,0))   # Text, AA , color
        screen.blit(the_text, (10, 10))     # draws text at 10,10

        if pygame.key.get_pressed()[27] == 1:
            menu()
        if pygame.key.get_pressed()[113] == 1:
            pygame.quit()
            break 
        my_clock = pygame.time.Clock()
        my_clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()     #Closes the windows and stops the music

main()