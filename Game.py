
import sys
import pygame
from pygame.locals import *
import os
import random

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Tile():
    def __init__(self, id, x, y, type, owner):
        self.Id = id
        self.X = x
        self.Y = y
        self.Type = type
        self.Owner = owner

def createBoard():
    for i in range(tiles):
        for j in range(tiles):
            tile = (screenX//tiles*j, screenY//tiles*i, screenX//tiles, screenY//tiles)
            if i == 0 or j == 0 or i == tiles-1 or j == tiles-1:
                if i == 0 and j == 0:
                    pygame.draw.rect(screen, players[0].Color, tile)
                elif i == tiles-1 and j == 0:
                    pygame.draw.rect(screen, players[1].Color, tile)
                elif i == 0 and j == tiles-1:
                    pygame.draw.rect(screen, players[3].Color, tile)
                elif i == tiles-1 and j == tiles-1:
                    pygame.draw.rect(screen, players[2].Color, tile)
                else:
                    pygame.draw.rect(screen,(0,200,255),tile, 10)
            else:
                pygame.draw.rect(screen,(255, 255, 255),tile)
    center = pygame.transform.scale(pygame.image.load('logo_super.png'), (screenX-(screenX//tiles*2), screenY-(screenY//tiles*2)))
    screen.blit(center, (screenX//tiles,screenY//tiles))

def createList(s, i, j):
    maxtile = tiles-1

    if i == 0 and j == 0:
        tilelist[s] = Tile(s, i, j, "corner", 0)
        createList(s+1, i, j+1)
    elif i == 0 and j > 0 and j < maxtile:
        tilelist[s] = Tile(s, i, j, "general", -1)
        createList(s+1, i, j+1)
    elif i == 0 and j == maxtile:
        tilelist[s] = Tile(s, i, j, "corner", 1)
        createList(s+1, i+1, j)
    elif i > 0 and i < maxtile and j == maxtile:
        tilelist[s] = Tile(s, i, j, "general", -1)
        createList(s+1, i+1, j)
    elif i == maxtile and j == maxtile:
        tilelist[s] = Tile(s, i, j, "corner", 2)
        createList(s+1, i, j-1)
    elif i == maxtile and j > 0 and j < maxtile:
        tilelist[s] = Tile(s, i, j, "general", -1)
        createList(s+1, i, j-1)
    elif i == maxtile and j == 0:
        tilelist[s] = Tile(s, i, j, "corner", 3)
        createList(s+1, i-1, j)
    elif i == 1 and j == 0:
        tilelist[s] = Tile(s, i, j, "general", -1)
    elif i > 0 and i < maxtile and j == 0:
        tilelist[s] = Tile(s, i, j, "general", -1)
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
    startB_text = my_font.render('RESUME GAME', True, (255,255,255))
    instructB_text = my_font.render('INSTRUCTIONS', True, (255,255,255))
    exitB_text = my_font.render("EXIT", True, (255,255,255))
    
    #draw text
    screen.blit(startB_text,(screenX//2-(len("RESUME GAME")*20), 50))
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
    background_text2 = font.render("2.To move your player press the 'Roll dice' button", True, (255,255,255))
    font = pygame.font.SysFont("Arial", 70)
    return_text = font.render('RETURN', True, (255,255,255))
    #draw text
    screen.blit(background_text1,(screenX//2-(len("1.Press the escape key to open the menu")*8), 150))
    screen.blit(background_text2,(screenX//2-(len("2.To move your player press the 'Roll dice' button")*8), 250))
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

class Player():
    def __init__(self, id, sprite, position, x, y, health, stamina, name, color, removed):
        self.Id = id
        self.Sprite = sprite
        self.Position = position
        self.X = x
        self.Y = y
        self.Health = health
        self.Stamina = stamina
        self.Name = name
        self.Color = color[id]
        self.Removed = removed

def playerCreate():
    players = {"":""}
    for s in range(0, numberOfPlayers):
        players[s] = Player(s, pygame.transform.scale(pygame.image.load(os.path.join("pawn24bit" + str(s+1) + ".png")), (screenX//tiles-10, screenY//tiles-10)), tilelist[(tiles-1)*s].Id, tilelist[(tiles-1)*s].X*(screenX//tiles)+5, tilelist[(tiles-1)*s].Y*(screenY//tiles)+5, 100, 15, "name", playerColors, False)
    global players

def playerMove(s, forward):
    if players[s].Position + forward > len(tilelist)-1:
        remainder = players[s].Position + forward - len(tilelist)-1
        players[s].Position = remainder
    players[s].Position += forward
    for i in range(len(tilelist)-1):
        if tilelist[i].Id == players[s].Position:
            players[s].X = tilelist[i].X*(screenX//tiles)+5
            players[s].Y = tilelist[i].Y*(screenY//tiles)+5
            pygame.display.flip()
            break

def turn(player):
    forward = random.randint(1,6)
    global playerN
    global forward
    if player == numberOfPlayers-1:
        playerMove(player, forward)
        checkFight(player)
        playerN = 0
    elif player < numberOfPlayers-1:
        playerMove(player, forward)
        checkFight(player)
        playerN += 1

def checkFight(player):
    for s in range(len(players)-1):
        if (players[player].Position == players[s].Position and players[player].Id != players[s].Id):
            fight(player, s, False)
    for s in range(len(tilelist)-1):
        if players[player].Position == tilelist[s].Id and tilelist[s].Type == "corner" and player != tilelist[s].Owner:
            fight(player, s, True)

def fight(player, defender, tile):
    pygame.display.flip()
    screen.fill((0, 0, 0))
    card1 = pygame.transform.scale(pygame.image.load(os.path.join("img", "sf" + str(player+1) + ".png")), (screenX, screenY))
    card2 = pygame.transform.scale(pygame.image.load(os.path.join("img", "sf" + str(random.randint(1,18)) + ".png")), (screenX, screenY))

    font = pygame.font.SysFont("Helvetica", 70)
    fight_rect = (0, screenY-(screenY//tiles), screenX, screenY//tiles)
    dice = pygame.transform.scale(pygame.image.load('die.png'), (screenX, screenY//tiles))

    if tile:
        versus = "It's Player " + str(players[player].Id) + " VS " + str(tilelist[defender].Owner)
        left_side = players[player].Color
        right_side = players[tilelist[defender].Owner].Color
    elif not tile:
        versus = "It's Player " + str(players[player].Id) + " VS " + str(players[defender].Id)
        left_side = players[player].Color
        right_side = players[defender].Color

    left_rect = (0, 0, screenX//2, screenY)
    right_rect = (screenX//2, 0, screenX//2, screenY)
    screen.fill(left_side, left_rect)
    screen.fill(right_side, right_rect)

    fight_text = font.render("Fight till death!", True, (255,255,255))
    versus_text = font.render(versus, True, (255,255,255))
    fight_button=screen.fill((0,0,0), fight_rect)
    screen.blit(fight_text, (screenX//2-(len("Fight till death")*12), 50))
    screen.blit(versus_text, (screenX//2-(len("It's player   VS   ")*12), 150))
    screen.blit(dice, (0, screenY-(screenY//tiles)))

    pygame.event.get()
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if fight_button.collidepoint(mpos) and b1 == 1:
        return
    if pygame.key.get_pressed()[27] == 1:
        menu()
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    fight(player, defender, tile)


def main():
    pygame.init()      # Prepare the pygame module for use
    pygame.display.set_caption('Fightclub')

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
    
    # for i in range(0,200):
    #   print(pygame.key.name(i), i)

    try:
        pygame.mixer.music.load('music.mp3') # Attempts to play music
        pygame.mixer.music.play(-1, 0.0)
    except:
        pass

    tilelist = {"": ""}
    tiles = 11
    numberOfPlayers = 4
    playerN = 0
    forward = 0
    playerColors = {0: (189,33,50), 1: (26,118,186), 2: (15,103,59), 3: (254,220,56)}
    global tilelist
    global tiles
    global numberOfPlayers
    global playerN
    global forward
    global playerColors
    createList(0,0,0)

    global screen
    playerCreate()
    menu()

    while True:
        pygame.display.flip()
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
        screen.fill((255, 255, 255))
        createBoard()

        pygame.event.pump()
        font = pygame.font.SysFont("Helvetica", 70)
        dice_rect = (screenX//2-screenX//tiles, screenY//tiles, screenX//tiles*2, screenY//tiles)
        dice_button=screen.fill(players[playerN].Color, dice_rect)
        dice_text = font.render(str(forward), True, (255,255,255))
        dice = pygame.transform.scale(pygame.image.load('die.png'), (screenX//tiles, screenY//tiles))
        screen.blit(dice_text, (screenX//2+(screenX//tiles//2), screenY//tiles))
        screen.blit(dice, (screenX//2-screenX//tiles,screenY//tiles))

        pygame.event.get()
        (b1,b2,b3) = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        if dice_button.collidepoint(mpos) and b1 == 1:
            turn(playerN)

        for s in range(numberOfPlayers):
            screen.blit(players[s].Sprite, (players[s].X, players[s].Y))

        pygame.event.get()
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