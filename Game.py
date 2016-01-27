import sys
import pygame
from pygame.locals import *
import os
import random
import pickle

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
                if (i == 0 and j == 0) or (i == 0 and j == 1) or (i == 1 and j == 0):
                    try:
                        pygame.draw.rect(screen, players[0].Color, tile)
                    except:
                        pass
                elif (i == tiles-1 and j == 0) or (i == tiles-1 and j == 1) or (i == tiles-2 and j == 0):
                    try:
                        pygame.draw.rect(screen, players[1].Color, tile)
                    except:
                        pass
                elif (i == 0 and j == tiles-1) or (i == 0 and j == tiles-2) or (i == 1 and j == tiles-1):
                    try:
                        pygame.draw.rect(screen, players[3].Color, tile)
                    except:
                        pass
                elif (i == tiles-1 and j == tiles-1) or (i == tiles-1 and j == tiles-2) or (i == tiles-2 and j == tiles-1):
                    try:
                        pygame.draw.rect(screen, players[2].Color, tile)
                    except:
                        pass
                else:
                    pygame.draw.rect(screen,(60,60,60),tile, 10)
            else:
                pygame.draw.rect(screen,(0, 0, 0),tile)
    center = pygame.transform.scale(pygame.image.load('boxing_ring_logo.png'), (screenX-(screenX//tiles*2), screenY-(screenY//tiles*2)))
    screen.blit(center, (screenX//tiles, screenY//tiles))

def createList(s, i, j):
    maxtile = tiles-1

    if numberOfPlayers >= 1:
        corner0 = "corner"
    else:
        corner0 = "general"
    if numberOfPlayers >= 2:
        corner1 = "corner"
    else:
        corner1 = "general"
    if numberOfPlayers >= 3:
        corner2 = "corner"
    else:
        corner2 = "general"
    if numberOfPlayers >= 4:
        corner3 = "corner"
    else:
        corner3 = "general"

    if i == 0 and j == 0: #topleft corner center
        tilelist[s] = Tile(s, i, j, corner0, 0)
        createList(s+1, i, j+1)
    elif i == 0 and j == 1: #topleft corner right
        tilelist[s] = Tile(s, i, j, corner0, 0)
        createList(s+1, i, j+1)
    elif i == 0 and j == tiles//2:
        tilelist[s] = Tile(s, i, j, "superfight", -1)
        createList(s+1, i, j+1)
    elif i == 0 and j == maxtile-1: #topright corner left
        tilelist[s] = Tile(s, i, j, corner1, 1)
        createList(s+1, i, j+1)
    elif i == 0 and j > 0 and j < maxtile:
        tilelist[s] = Tile(s, i, j, "general", -1)
        createList(s+1, i, j+1)
    elif i == 0 and j == maxtile: #topright corner center
        tilelist[s] = Tile(s, i, j, corner1, 1)
        createList(s+1, i+1, j)
    elif i == 1 and j == maxtile: #topright corner bottom
        tilelist[s] = Tile(s, i, j, corner1, 1)
        createList(s+1, i+1, j)
    elif i == tiles//2 and j == maxtile:
        tilelist[s] = Tile(s, i, j, "superfight", -1)
        createList(s+1, i+1, j)
    elif i == maxtile-1 and j == maxtile: #bottomright corner top
        tilelist[s] = Tile(s, i, j, corner2, 2)
        createList(s+1, i+1, j)
    elif i > 0 and i < maxtile and j == maxtile:
        tilelist[s] = Tile(s, i, j, "general", -1)
        createList(s+1, i+1, j)
    elif i == maxtile and j == maxtile: #bottomright corner center
        tilelist[s] = Tile(s, i, j, corner2, 2)
        createList(s+1, i, j-1)
    elif i == maxtile and j == maxtile-1: #bottomright corner left
        tilelist[s] = Tile(s, i, j, corner2, 2)
        createList(s+1, i, j-1)
    elif i == maxtile and j == tiles//2:
        tilelist[s] = Tile(s, i, j, "superfight", -1)
        createList(s+1, i, j-1)
    elif i == maxtile and j == maxtile-1: #bottomleft corner right
        tilelist[s] = Tile(s, i, j, corner3, 3)
        createList(s+1, i, j-1)
    elif i == maxtile and j > 0 and j < maxtile:
        tilelist[s] = Tile(s, i, j, "general", -1)
        createList(s+1, i, j-1)
    elif i == maxtile and j == 0: #bottomleft corner center
        tilelist[s] = Tile(s, i, j, corner3, 3)
        createList(s+1, i-1, j)
    elif i == maxtile-1 and j == 0: #bottomleft corner top
        tilelist[s] = Tile(s, i, j, corner3, 3)
        createList(s+1, i-1, j)
    elif i == 1 and j == 0: #topleft corner bottom
        tilelist[s] = Tile(s, i, j, corner0, 0)
    elif i == tiles//2 and j == 0:
        tilelist[s] = Tile(s, i, j, "superfight", -1)
        createList(s+1, i-1, j)
    elif i > 0 and i < maxtile and j == 0:
        tilelist[s] = Tile(s, i, j, "general", -1)
        createList(s+1, i-1, j)

def menu():
    pygame.display.flip()
    black = (0, 0, 0, 0)
    red = (150, 0, 0)
    data1 = []
    screen.fill(red)
    logotexture = pygame.transform.scale(pygame.image.load('boxing_ring_logo.png'), (screenX, screenY))
    screen.blit(logotexture, (0,0))

    #buttons (x, y, size x, size y)
    start_rect = (0, 50, screenX//2.5, 75)
    manual_rect = (0, 150, screenX//2.5, 75)
    save_rect = (0, 250, screenX//2.5, 75)
    load_rect = (0, 350, screenX//2.5, 75)
    exit_rect = (0, 550, screenX//2.5, 75) 

    start_button = screen.fill(black, start_rect)
    instruct_button = screen.fill(black, manual_rect)
    save_button = screen.fill(black, save_rect)
    load_button = screen.fill(black, load_rect)
    exit_button = screen.fill(black, exit_rect)

    #load images
    startB_img = pygame.transform.scale(pygame.image.load('b_start.png'), (screenX//2, 75))
    manualB_img = pygame.transform.scale(pygame.image.load('b_manual.png'), (screenX//2, 75))
    saveB_img = pygame.transform.scale(pygame.image.load('b_save.png'), (screenX//2, 75))
    loadB_img = pygame.transform.scale(pygame.image.load('b_load.png'), (screenX//2, 75))
    exitB_img = pygame.transform.scale(pygame.image.load('b_exit.png'), (screenX//2, 75))
    
    #draw images
    screen.blit(startB_img, (0, 50))
    screen.blit(manualB_img, (0, 150))
    screen.blit(saveB_img, (0, 250))
    screen.blit(loadB_img, (0, 350))
    screen.blit(exitB_img, (0, 550))

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if start_button.collidepoint(mpos) and b1==1:
        return
    if instruct_button.collidepoint(mpos) & b1==1:
        instructions()
    if save_button.collidepoint(mpos) & b1==1:
        for s in range(numberOfPlayers):
            data1.append(players[s].Id)
            data1.append(players[s].Position)
            data1.append(players[s].X)
            data1.append(players[s].Y)
            data1.append(players[s].Health)
            data1.append(players[s].Stamina)
            data1.append(players[s].Card)
            data1.append(players[s].Color)
            data1.append(players[s].Removed)
            data1.append(players[s].Name)
        with open('savefile', 'wb') as f:
            pickle.dump(data1, f)
        print("Saved!")
    if load_button.collidepoint(mpos) & b1==1:
        with open('savefile', 'rb') as f:
            data1 = pickle.load(f)
        for s in range(numberOfPlayers):        #id, sprite, position, x, y, health, stamina, name, color, removed):
            print("Imported:", data1[s*10])
            players[s].Id = data1[s*10]
            players[s].Position = data1[s*10+1]
            players[s].X = data1[s*10+2]
            players[s].Y = data1[s*10+3]
            players[s].Health = data1[s*10+4]
            players[s].Stamina = data1[s*10+5]
            players[s].Card = data1[s*10+6]
            players[s].Color = data1[s*10+7]
            players[s].Removed = data1[s*10+8]
            players[s].Name = data1[s*10+9]
            global players
        print("Loaded!")
        return
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
    logotexture = pygame.transform.scale(pygame.image.load('manual.png'), (screenX, screenY))
    screen.blit(logotexture, (0,0))

    return_rect = (0, screenY-100, screenX, 75)
    return_button=screen.fill(black, return_rect)
    #text Text, AA , color
    font = pygame.font.SysFont("Arial", 70)
    return_text = font.render('RETURN', True, (255,255,255))
    #draw text
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
    def __init__(self, id, sprite, position, x, y, health, stamina, card, color, removed, name):
        self.Id = id
        self.Sprite = sprite
        self.Position = position
        self.X = x
        self.Y = y
        self.Health = health
        self.Stamina = stamina
        self.Card = card
        self.Color = color[id]
        self.Removed = removed
        self.Name = name

def playerCreate():
    players = {"":""}
    for s in range(0, numberOfPlayers):
        players[s] = Player(s, pygame.transform.scale(pygame.image.load(os.path.join("pawns", "pawn" + str(s+1) + "-8bit.png")), (screenX//tiles-10, screenY//tiles-10)), tilelist[(tiles-1)*s].Id, tilelist[(tiles-1)*s].X*(screenX//tiles)+5, tilelist[(tiles-1)*s].Y*(screenY//tiles)+5, 100, 15, s, playerColors, False, cardName[s])
    global players

def playerMove(s, forward):
    if players[s].Position + forward > len(tilelist)-2:
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
    forward = 1
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
        if players[player].Position == tilelist[s].Id and tilelist[s].Type == "corner" and player == tilelist[s].Owner:
            players[player].Stamina = 15
            print("Player", player, "'s Stamina is now:", players[player].Stamina)
            break
        if players[player].Position == tilelist[s].Id and tilelist[s].Type == "corner" and player != tilelist[s].Owner:
            fight(player, s, True)

def fight(player, defender, tile):
    pygame.display.flip()
    screen.fill((0, 0, 0))
    card1 = pygame.transform.scale(pygame.image.load(os.path.join("img", "sf" + str(player+1) + ".png")), (screenX//3, screenY//3))
    # card2 = pygame.transform.scale(pygame.image.load(os.path.join("img", "sf" + str(random.randint(1,18)) + ".png")), (screenX//3, screenY//3))
    card2 = pygame.transform.scale(pygame.image.load(os.path.join("img", "sf" + str(defender+1) + ".png")), (screenX//3, screenY//3))

    font = pygame.font.SysFont("Helvetica", 70)
    fight_rect = (0, screenY-(screenY//tiles), screenX, screenY//tiles)
    button_fight = pygame.transform.scale(pygame.image.load('button_fight.png'), (screenX//tiles, screenY//tiles))

    if tile:
        versus = "It's Player " + str(players[player].Id) + " VS " + str(tilelist[defender].Owner)
        right_side = players[tilelist[defender].Owner].Color
    elif not tile:
        versus = "It's Player " + str(players[player].Id) + " VS " + str(players[defender].Id)
        right_side = players[defender].Color

    left_side = players[player].Color
    left_rect = (0, 0, screenX//2, screenY)
    right_rect = (screenX//2, 0, screenX//2, screenY)
    screen.fill(left_side, left_rect)
    screen.fill(right_side, right_rect)

    #Draws the options for the cards to pick
    s = 0
    for i in range(2):
        if i == 0:
            p = player
        elif tile:
            p = players[tilelist[defender].Owner].Id
        else:
            p = defender
        for s in range(len(cardAttacks[s])):
            font = pygame.font.SysFont("Helvetica", 45)
            cardNameText = "Attack " + str(s+1)
            name_text = font.render(cardNameText, True, (255,255,255))

            font = pygame.font.SysFont("Helvetica", 14)
            cardDamageText = "Damage: " + str(cardAttacks[p][s+1])
            cardStaminaText = "Required Stamina: " + str(cardStamina[p][s+1])
            damage_text = font.render(cardDamageText, True, (255,255,255))
            stamina_text = font.render(cardStaminaText, True, (255,255,255))

            choice_rect = (100+(screenX//2)*i+1, (screenY//2)+100*s, screenX//5, 75)
            choice_button=screen.fill((0,0,0), choice_rect)
            screen.blit(name_text, (110+(screenX//2)*i+1, (screenY//2)+100*s))
            screen.blit(damage_text, (120+(screenX//2)*i+1, (screenY//2)+45+100*s))
            screen.blit(stamina_text, (120+(screenX//2)*i+1, (screenY//2)+60+100*s))

    font = pygame.font.SysFont("Helvetica", 70)
    versus_text = font.render("VS", True, (255,255,255))
    fight_button=screen.fill((0,0,0), fight_rect)
    screen.blit(versus_text, (screenX//2-(len("VS")*25), 100))
    screen.blit(button_fight, (screenX//2-screenX//tiles//2, screenY-(screenY//tiles)))
    screen.blit(card1, ((screenX//tiles), screenY//tiles))
    screen.blit(card2, ((screenX//2+screenX//tiles, screenY//tiles)))

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

def finish(s):
    black = (0, 0, 0)
    pygame.display.flip()
    font = pygame.font.SysFont('Arial',60,True)
    text = font.render("Game finished", True, (0,255,255))
    win_play = font.render("Player {0} won" .format(s), True, (0,255,255))
    exitB_text = font.render("EXIT", True, (255,255,255))
    exit_rect = (0, screenY//2, screenX, 75)
    exit_button=screen.fill(black, exit_rect)
    screen.blit(text,(screenX//2-(len('Game finished')*13), 150))
    screen.blit(win_play,(screenX//2-(len('Game finished')*13), 280))
    screen.blit(exitB_text, (screenX//2-(len("EXIT")*4), screenY//2))
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if exit_button.collidepoint(mpos) and b1==1:
        pygame.quit()
    pygame.event.wait()
    finish(s)

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
    screen = pygame.display.set_mode((screenX, screenY), HWSURFACE)
    global screenX
    global screenY

    cardName = {0:"Rocky Belboa", 1:"Manny Pecquiao", 2:"Mike Tysen", 3:"Badr Heri"}

    cardAttacks = {0: {1:12, 2:18, 3:30},
        1: {1:8, 2:22, 3:30},
        2: {1:10, 2:20, 3:30},
        3: {1:10, 2:18, 3:32}}

    cardStamina = {0: {1:3, 2:6, 3:9},
        1: {1:3, 2:6, 3:9},
        2: {1:3, 2:6, 3:9},
        3: {1:3, 2:6, 3:9}}

    global cardName
    global cardAttacks
    global cardStamina
    
    # for i in range(0,200):
    #   print(pygame.key.name(i), i)

    pygame.mixer.init(44100, -16,2,2048)

    try:
        pygame.mixer.music.load('music.wav') # Attempts to play music
        # pygame.mixer.music.play(-1, 0.0)
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
        screen.fill((0, 0, 0))
        createBoard()

        pygame.event.pump()
        font = pygame.font.SysFont("Helvetica", 70)
        dice_rect = (screenX//2-screenX//tiles, screenY//tiles, screenX//tiles*2, screenY//tiles)
        dice_button=screen.fill(players[playerN].Color, dice_rect)
        dice_text = font.render(str(forward), True, (255,255,255))
        dice = pygame.transform.scale(pygame.image.load('die.png'), (screenX//tiles, screenY//tiles))
        font = pygame.font.SysFont("Helvetica", 40)
        playerStat = font.render('Player: {0}' .format(players[playerN].Name), True, players[playerN].Color)
        healthStat = font.render('Health: {0}' .format(players[playerN].Health), True, players[playerN].Color)
        staminaStat = font.render('Stamina: {0}' .format(players[playerN].Stamina), True, players[playerN].Color)

        screen.blit(dice_text, (screenX//2+(screenX//tiles//2), screenY//tiles))
        screen.blit(dice, (screenX//2-screenX//tiles,screenY//tiles))
        screen.blit(playerStat, (screenX//tiles, screenY//tiles+20))
        screen.blit(healthStat, (screenX//tiles, screenY//tiles+80))
        screen.blit(staminaStat, (screenX//tiles, screenY//tiles+140))

        pygame.event.get()
        (b1,b2,b3) = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        if dice_button.collidepoint(mpos) and b1 == 1:
            turn(playerN)

        data1 = []
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