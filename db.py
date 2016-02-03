import sys
import pygame
from pygame.locals import *
import sqlite3          #------------------------------sqlite
import os
import random
import pickle
from time import *

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
database = 'test.db'    #-------------------------------database
os.chdir(dname)

if os.path.isfile(database) == False:           #--------creates database and table
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    sql_command = """
    CREATE TABLE player(
    Id INTEGER,
    Position INTEGER,
    X INTEGER,
    Y INTEGER,
    Health INTEGER,
    Stamina INTEGER,
    Card INTEGER,
    Removed INTEGER,
    Name VARCHAR(30),
    R INTEGER,
    G INTEGER,
    B INTEGER);"""
    cursor.execute(sql_command)
else:
    connection = sqlite3.connect(database)
    cursor = connection.cursor()                #---------end

class Tile():
    def __init__(self, id, x, y, type, owner):
        self.Id = id
        self.X = x
        self.Y = y
        self.Type = type
        self.Owner = owner

def createBoard():
    superfightImg = pygame.transform.scale(pygame.image.load("button_fight.png"), (screenX//tiles, screenY//tiles))
    grey = (60, 60, 60)
    red = (120, 20, 0)
    for i in range(tiles):
        for j in range(tiles):
            tile = (screenX//tiles*j, screenY//tiles*i, screenX//tiles, screenY//tiles)
            if i == 0 or j == 0 or i == tiles-1 or j == tiles-1:
                if (i == 0 and j == 0) or (i == 0 and j == 1) or (i == 1 and j == 0):
                    try:
                        pygame.draw.rect(screen, players[0].Color, tile)
                    except:
                        pygame.draw.rect(screen, grey, tile, 10)
                elif (i == tiles-1 and j == 0) or (i == tiles-1 and j == 1) or (i == tiles-2 and j == 0):
                    try:
                        pygame.draw.rect(screen, players[1].Color, tile)
                    except:
                        pygame.draw.rect(screen, grey, tile, 10)
                elif (i == 0 and j == tiles-1) or (i == 0 and j == tiles-2) or (i == 1 and j == tiles-1):
                    try:
                        pygame.draw.rect(screen, players[3].Color, tile)
                    except:
                        pygame.draw.rect(screen, grey,tile, 10)
                elif (i == tiles-1 and j == tiles-1) or (i == tiles-1 and j == tiles-2) or (i == tiles-2 and j == tiles-1):
                    try:
                        pygame.draw.rect(screen, players[2].Color, tile)
                    except:
                        pygame.draw.rect(screen, grey,tile, 10)
                elif (i == 0 and j == tiles//2) or (i == tiles//2 and j == tiles-1) or (i == tiles-1 and j == tiles//2) or (i == tiles//2 and j == 0):
                    pygame.draw.rect(screen, red, tile, 10)
                    screen.blit(superfightImg, tile)
                else:
                    pygame.draw.rect(screen, grey,tile, 10)
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
    black = (0, 0, 0)
    white = (255, 255, 255)
    data1 = []
    data2 = []                  ##############
    global bCurrentImage
    global music_playing
    global players

    animationImg = pygame.transform.scale(pygame.image.load(os.path.join("anime", "an" + str(bCurrentImage) + ".png")), (screenX, screenY))
    screen.blit(animationImg, (0,0))
    if bCurrentImage < 9:
        bCurrentImage += 1
    else:
        bCurrentImage = 1

    my_font = pygame.font.SysFont("Arial", 70)
    if os.path.isfile("savefile"):
        start_button = Rect(0, 150, screenX//2.5, 75)
        startB_text = my_font.render('RESUME SAVED GAME', True, (255,255,255))
        screen.blit(startB_text,(0, 150))

    #buttons (x, y, size x, size y)
    new_button = Rect(0, 50, screenX//2.5, 75)
    instruct_button = Rect(0, 250, screenX//2.5, 75)
    save_button = Rect(0, 350, screenX//2.5, 75)
    load_button = Rect(0, 450, screenX//2.5, 75)
    settings_button = Rect(0, 550, screenX//2.5, 75)
    exit_button = Rect(0, 650, screenX//2.5, 75)

    #text Text, AA , color
    newB_text = my_font.render('NEW GAME', True, (255,255,255))
    instructB_text = my_font.render('INSTRUCTIONS', True, (255,255,255))
    saveB_text = my_font.render('SAVE', True, (255,255,255))
    loadB_text = my_font.render('LOAD', True, (255,255,255))
    settingsB_text = my_font.render('SETTINGS', True, (255,255,255))
    exitB_text = my_font.render("EXIT", True, (255,255,255))

    #draw text
    screen.blit(newB_text,(0, 50))
    screen.blit(instructB_text,(0, 250))
    screen.blit(saveB_text,(0, 350))
    screen.blit(loadB_text,(0, 450))
    screen.blit(settingsB_text,(0,550))
    screen.blit(exitB_text, (0, 650))

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if new_button.collidepoint(mpos) & b1==1:
        return newGame()
    if os.path.isfile("savefile"):
        if start_button.collidepoint(mpos) and b1==1:
            connection = sqlite3.connect(database)  #-- connection to database
            cursor = connection.cursor()            #--

            createList(0,0,0)
            playerCreate()
            with open('savefile', 'rb') as f:
                data2 = pickle.load(f)              ##############
            music_playing = data2[0]                #####################
            print("0:", data2[0])                   ####################
            for s in range(0,numberOfPlayers):

                dat = cursor.execute('SELECT * FROM player WHERE Id={}'.format(s))                      #-------------- data load
                id, position, x, y, health, stamina, card, removed, name, r, g, b = dat.fetchone()
                players[s].Id = id
                players[s].Position = position
                players[s].X = x
                players[s].Y = y
                players[s].Health = health
                players[s].Stamina = stamina
                players[s].Card = card
                players[s].Removed = removed
                players[s].Name = name
                players[s].Color = (r,g,b)                                                              #--------------

                global players
                global music_playing
            if not music_playing:
                pygame.mixer.music.stop()
                music_playing = False
            else:
                try:
                    pygame.mixer.music.play(-1, 0.0)
                    music_playing = True
                except:
                    pass
            print("Loaded!")
            return

    if instruct_button.collidepoint(mpos) & b1==1:
        instructions()


    if save_button.collidepoint(mpos) & b1==1:
        data2.append(music_playing)             ###############
        connection = sqlite3.connect(database)  #-- connection to database
        cursor = connection.cursor()            #--

        cursor.execute('DROP TABLE IF EXISTS player')       #-------drops table
                                                        #-----------creates new table
        sql_command = """
        CREATE TABLE player(
        Id INTEGER,
        Position INTEGER,
        X INTEGER,
        Y INTEGER,
        Health INTEGER,
        Stamina INTEGER,
        Card INTEGER,
        Removed INTEGER,
        Name VARCHAR(30),
        R INTEGER,
        G INTEGER,
        B INTEGER);"""
        cursor.execute(sql_command)         #---------------------------

        for s in range(0,numberOfPlayers):
            R, G, B = players[s].Color      #--------added
            data1.append(players[s].Id)
            data1.append(players[s].Position)
            data1.append(players[s].X)
            data1.append(players[s].Y)
            data1.append(players[s].Health)
            data1.append(players[s].Stamina)
            data1.append(players[s].Card)
            data1.append(players[s].Removed)
            data1.append(players[s].Name)
            data1.append(R)
            data1.append(G)
            data1.append(B)     #----------------------------
        it = [iter(data1)] * 12         #--------- creates list of tuples
        data=list(zip(*it))
        print(data)                     #---------

        cursor.executemany('INSERT INTO player VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',data)      #-------------inserts data

        connection.commit()                   #------- commits it

        cursor.execute("SELECT * FROM player")      #---prints all data in database
        print("fetchall:")
        result = cursor.fetchall()
        for r in result:
            print(r)
                                                    #------------------------------------
        print(data1)
        with open('savefile', 'wb') as f:
            pickle.dump(data2, f)           ################
        print("Saved!")


    if load_button.collidepoint(mpos) & b1==1:
        connection = sqlite3.connect(database)  #-- connection to database
        cursor = connection.cursor()            #--

        createList(0,0,0)
        playerCreate()
        with open('savefile', 'rb') as f:
            data2 = pickle.load(f)          ########################
        music_playing = data2[0]               ##################
        for s in range(0,numberOfPlayers):

            dat = cursor.execute('SELECT * FROM player WHERE Id={}'.format(s))                      #-------------- data load
            id, position, x, y, health, stamina, card, removed, name, r, g, b = dat.fetchone()
            players[s].Id = id
            players[s].Position = position
            players[s].X = x
            players[s].Y = y
            players[s].Health = health
            players[s].Stamina = stamina
            players[s].Card = card
            players[s].Removed = removed
            players[s].Name = name
            players[s].Color = (r,g,b)                                                              #--------------

            global players
            global music_playing

        if not music_playing:
            pygame.mixer.music.stop()
            music_playing = False
        else:
            try:
                pygame.mixer.music.play(-1, 0.0)
                music_playing = True
            except:
                pass
        print("Loaded!")
        return
    if settings_button.collidepoint(mpos) and b1==1:
        settings()
    if exit_button.collidepoint(mpos) and b1==1:
        pygame.quit()
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    return menu()

def newGame():
    pygame.display.flip()
    black = (0, 0, 0)
    red = (150, 0, 0)
    screen.fill(red)
    logotexture = pygame.transform.scale(pygame.image.load('boxing_ring_logo.png'), (screenX, screenY))
    screen.blit(logotexture, (0,0))
    global ng
    global music_playing
    global numberOfPlayers

    #buttons (x, y, size x, size y)
    start_button = Rect(screenX - screenX//2.5,50,screenX//2.5, 75)
    p_button = Rect(screenX - screenX//2.5, 150, screenX//2.5, 75)
    return_button = Rect(screenX - screenX//2.5, 550, screenX//2.5, 75)

    #text Text, AA , color
    my_font = pygame.font.SysFont("Arial", 70)
    startB_text = my_font.render('NEXT', True, (255,255,255))
    pB_text = my_font.render('PLAYERS: {0}' .format(numberOfPlayers), True, (255,255,255))
    returnB_text = my_font.render("RETURN", True, (255,255,255))

    #draw text
    screen.blit(startB_text,(screenX - screenX//2.5, 50))
    screen.blit(pB_text,(screenX - screenX//2.5, 150))
    screen.blit(returnB_text, (screenX - screenX//2.5, 550))

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if start_button.collidepoint(mpos) and b1==1:
        chooseCardScreen()
    if p_button.collidepoint(mpos) and b1==1:
        if numberOfPlayers <4:
            numberOfPlayers += 1
        else:
            numberOfPlayers = 2
    if return_button.collidepoint(mpos) and b1==1:
        return
    if pygame.key.get_pressed()[27] == 1:
        return
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    if ng == True:
        return
    pygame.event.wait()
    newGame()

def chooseCardScreen():
    pygame.display.flip()
    black = (0, 0, 0)
    red = (150, 0, 0)
    screen.fill(red)
    logotexture = pygame.transform.scale(pygame.image.load('boxing_ring_logo.png'), (screenX, screenY))
    screen.blit(logotexture, (0,0))
    global ng
    global music_playing
    global numberOfPlayers


    #buttons (x, y, size x, size y)
    start_button = Rect(0,50,screenX//2.5, 75)
    return_button = Rect(0, 550, screenX//2.5, 75)

    #text Text, AA , color
    my_font = pygame.font.SysFont("Arial", 70)
    startB_text = my_font.render('START', True, (255,255,255))
    returnB_text = my_font.render("RETURN", True, (255,255,255))

    #draw text
    screen.blit(startB_text,(0, 50))
    screen.blit(returnB_text, (0, 550))

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if start_button.collidepoint(mpos) and b1==1:
        ng = True
        createList(0,0,0)
        playerCreate()
        return
    if return_button.collidepoint(mpos) and b1==1:
        return
    if pygame.key.get_pressed()[27] == 1:
        return
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    chooseCardScreen()

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

def settings():
    pygame.display.flip()
    black = (0, 0, 0)
    red = (150, 0, 0)
    screen.fill(red)
    logotexture = pygame.transform.scale(pygame.image.load('boxing_ring_logo.png'), (screenX, screenY))
    screen.blit(logotexture, (0,0))
    global music_playing

    #buttons (x, y, size x, size y)
    mute_button = Rect(screenX-screenX//2.5, 50,screenX//2.5, 75)
    return_button = Rect(screenX-screenX//2.5, 550, screenX//2.5, 75)

    #text Text, AA , color
    my_font = pygame.font.SysFont("Arial", 70)
    muteB_text = my_font.render('MUTE', True, (255,255,255))
    returnB_text = my_font.render("RETURN", True, (255,255,255))

    #draw text
    screen.blit(muteB_text,(screenX-screenX//2.5, 50))
    screen.blit(returnB_text, (screenX-screenX//2.5, 550))

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if mute_button.collidepoint(mpos) and b1==1:
        if music_playing:
            pygame.mixer.music.stop()
            music_playing = False
        else:
            try:
                pygame.mixer.music.play(-1, 0.0)
                music_playing = True
            except:
                pass
    if return_button.collidepoint(mpos) and b1==1:
        return
    if pygame.key.get_pressed()[27] == 1:
        return
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    return settings()

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
    pickedCards = {1: -1, 2: -1}
    global pickedCards
    forward = random.randint(1,6)
    global playerN
    global forward
    if players[player].Removed == True:
        if player == numberOfPlayers-1:
            playerN = 0
        elif player < numberOfPlayers-1:
            playerN += 1
    if player == numberOfPlayers-1:
        playerMove(player, forward)
        checkFight(player)
        playerN = 0
    elif player < numberOfPlayers-1:
        playerMove(player, forward)
        checkFight(player)
        playerN += 1

def checkFight(player):
    for s in range(len(tilelist)-1):
        if players[player].Position == tilelist[s].Id and tilelist[s].Type == "superfight":
            superFight(player)
        elif players[player].Position == tilelist[s].Id and tilelist[s].Type == "corner" and player == tilelist[s].Owner:
            players[player].Stamina = 15
            break
        elif players[player].Position == tilelist[s].Id and tilelist[s].Type == "corner" and player != tilelist[s].Owner:
            fight(player, s, True)
        else:
            for s in range(len(players)-1):
                if (players[player].Position == players[s].Position and players[player].Id != players[s].Id):
                    fight(player, s, False)

def superFight(player):
    pygame.display.flip()
    screen.fill((0,0,0))
    superfighter = random.randint(1,17)
    card1 = pygame.transform.scale(pygame.image.load(os.path.join("player_cards", "p" + str(player+1) + ".png")), (screenX//3, screenY//3))
    card2 = pygame.transform.scale(pygame.image.load(os.path.join("img", "sf" + str(superfighter) + ".png")), (screenX//3, screenY//3))
    pickedSFCard = -1
    global pickedSFCard

    font = pygame.font.SysFont("Helvetica", 70)
    background = players[player].Color
    background_rect = (0, 0, screenX, screenY)
    screen.fill(background, background_rect)

    #Draws the options for the cards to pick
    s = 0
    choice_button = {1:[]}
    for s in range(len(cardAttacks[s])):
        font = pygame.font.SysFont("Helvetica", 45)
        cardNameText = "Attack " + str(s+1)
        name_text = font.render(cardNameText, True, (255,255,255))

        font = pygame.font.SysFont("Helvetica", 14)
        cardDamageText = "Damage: " + str(cardAttacks[player][s+1])
        cardStaminaText = "Required Stamina: " + str(cardStamina[player][s+1])
        damage_text = font.render(cardDamageText, True, (255,255,255))
        stamina_text = font.render(cardStaminaText, True, (255,255,255))
        choice_rect = Rect(100, (screenY//2)+100*s, screenX//5, 75)
        choice_button[1].append(screen.fill((0,0,0), choice_rect))

        screen.blit(name_text, (110, (screenY//2)+100*s))
        screen.blit(damage_text, (120, (screenY//2)+45+100*s))
        screen.blit(stamina_text, (120, (screenY//2)+60+100*s))

    font = pygame.font.SysFont("Helvetica", 70)
    versus_text = font.render("VS", True, (255,255,255))
    screen.blit(versus_text, (screenX//2-(len("VS")*25), 100))
    screen.blit(card1, ((screenX//tiles), screenY//tiles))
    screen.blit(card2, ((screenX//2+screenX//tiles, screenY//tiles)))

    pygame.event.get()
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    for s in range(len(cardAttacks[s])):
        if choice_button[1][s].collidepoint(mpos) and b1 == 1:
            pickedSFCard = s+1

    if pickedSFCard != -1:
        superFightResult(player, superfighter, pickedSFCard)
        return
    if pygame.key.get_pressed()[27] == 1:
        menu()
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    superFight(player)

def fight(player, defender, tile):
    pygame.display.flip()
    screen.fill((0, 0, 0))
    card1 = pygame.transform.scale(pygame.image.load(os.path.join("player_cards", "p" + str(player+1) + ".png")), (screenX//3, screenY//3))
    print(tilelist[defender].Type)
    global pickedCards
    font = pygame.font.SysFont("Helvetica", 70)

    if tile:
        versus = "It's Player " + str(players[player].Id) + " VS " + str(tilelist[defender].Owner)
        right_side = players[tilelist[defender].Owner].Color
        card2 = pygame.transform.scale(pygame.image.load(os.path.join("player_cards", "p" + str(tilelist[defender].Owner+1) + ".png")), (screenX//3, screenY//3))
    elif not tile:
        versus = "It's Player " + str(players[player].Id) + " VS " + str(players[defender].Id)
        right_side = players[defender].Color
        card2 = pygame.transform.scale(pygame.image.load(os.path.join("player_cards", "p" + str(defender+1) + ".png")), (screenX//3, screenY//3))

    left_side = players[player].Color
    left_rect = (0, 0, screenX//2, screenY)
    right_rect = (screenX//2, 0, screenX//2, screenY)
    screen.fill(left_side, left_rect)
    screen.fill(right_side, right_rect)

    #Draws the options for the cards to pick
    s = 0
    choice_button = {1:[],2:[]}
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
            choice_rect = Rect(100+(screenX//2)*i+1, (screenY//2)+100*s, screenX//5, 75)
            choice_button[i+1].append(screen.fill((0,0,0), choice_rect))

            screen.blit(name_text, (110+(screenX//2)*i+1, (screenY//2)+100*s))
            screen.blit(damage_text, (120+(screenX//2)*i+1, (screenY//2)+45+100*s))
            screen.blit(stamina_text, (120+(screenX//2)*i+1, (screenY//2)+60+100*s))

    font = pygame.font.SysFont("Helvetica", 70)
    versus_text = font.render("VS", True, (255,255,255))
    screen.blit(versus_text, (screenX//2-(len("VS")*25), 100))
    screen.blit(card1, ((screenX//tiles), screenY//tiles))
    screen.blit(card2, ((screenX//2+screenX//tiles, screenY//tiles)))

    pygame.event.get()
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    for i in range(2):
        for s in range(len(cardAttacks[s])):
            if choice_button[i+1][s].collidepoint(mpos) and b1 == 1:
                pickedCards[i+1] = s+1
    # print(tile)
    if pickedCards[1] != -1 and pickedCards[2] != -1 and tile:
        fightResult(player, players[tilelist[defender].Owner].Id, pickedCards[1], pickedCards[2], tile)
        return
    elif pickedCards[1] != -1 and pickedCards[2] != -1 and not tile:
        fightResult(player, defender, pickedCards[1], pickedCards[2], tile)
        return
    print("Variables:", player, defender, pickedCards[1], pickedCards[2], tile)
    if pygame.key.get_pressed()[27] == 1:
        menu()
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    fight(player, defender, tile)

def superFightResult(player, defender, pickedCard):
    if not players[player].Stamina - cardStamina[player][pickedCard] < 0:
        if cardAttacks[player][pickedCard] < sfDamage[defender]:
            players[player].Health -= sfDamage[defender]
            players[player].Stamina -= cardStamina[player][pickedCard]
            print("Player", player, "'s health is now", players[player].Health, "because SF", defender, "dealt", sfDamage[defender], "damage.")
        else:
            players[player].Stamina -= cardStamina[player][pickedCard]
    else:
        players[player].Health -= sfDamage[defender]
    global players
    checkHealth()
    return

def fightResult(attacker, defender, attackerCard, defenderCard, tile):
    if not players[attacker].Stamina - cardStamina[attacker][attackerCard] < 0:
        players[defender].Health -= cardAttacks[attacker][attackerCard]
        players[attacker].Stamina -= cardStamina[attacker][attackerCard]
    print(players[defender])
    print(cardStamina[defender])
    print(cardStamina[defender][defenderCard])
    if not players[defender].Stamina - cardStamina[defender][defenderCard] < 0:
        players[attacker].Health -= cardAttacks[defender][defenderCard]
        players[defender].Stamina -= cardStamina[defender][defenderCard]
    global players
    # pickedCards = {1: -1, 2: -1}
    # global pickedCards
    # players[0].Health = 2
    # players[1].Health = 0
    # players[2].Health = 100
    # players[3].Health = 0
    checkHealth()
    return

def checkHealth():
    playersHealthList = {}
    for s in range(numberOfPlayers):
        if players[s].Health > 0:
            playersHealthList[s] = players[s].Health
        else:
            players[s].Removed = True
            activePlayers -= 1
            global activePlayers
    if activePlayers == 1:
        listValues = list(playersHealthList.values())
        listKeys = list(playersHealthList.keys())
        winner = listKeys[listValues.index(max(listValues))]

        while True:
            font = pygame.font.SysFont('Arial', 200, True)
            winner_text = font.render("Player {0} won!" .format(winner), True, players[winner].Color)
            winBackground = pygame.transform.scale(pygame.image.load('boxing_ring.jpg'), (screenX, screenY))
            exit_rect = Rect(screenX//2-(screenX//tiles*1.5), screenY-(screenY//tiles*3), screenX//tiles*3, screenY//tiles)
            exit_text = pygame.transform.scale(pygame.image.load('b_exit.png'), (screenX//tiles*3, screenY//tiles))
            screen.blit(winBackground, (0, 0))
            screen.blit(winner_text, (0, 0))
            exit_button = screen.fill((0,0,0), exit_rect)
            screen.blit(exit_text, (screenX//2-(screenX//tiles*1.5), screenY-(screenY//tiles*3)))
            pygame.display.flip()

            pygame.event.wait()
            pygame.event.get()
            (b1,b2,b3) = pygame.mouse.get_pressed()
            mpos = pygame.mouse.get_pos()
            if (exit_button.collidepoint(mpos) and b1 == 1) or pygame.key.get_pressed()[27] == 1:
                return main()
            if pygame.key.get_pressed()[113] == 1:
                pygame.quit()
                break
        return main()
    return

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
    global screen

    cardName = {0:"Rocky Belboa", 1:"Mike Tysen", 2:"Badr Heri", 3:"Manny Pecquiao"}

    cardAttacks = {0: {1:12, 2:18, 3:30},
        1: {1:8, 2:22, 3:30},
        2: {1:10, 2:20, 3:30},
        3: {1:10, 2:18, 3:32}}

    cardStamina = {0: {1:3, 2:6, 3:9},
        1: {1:3, 2:6, 3:9},
        2: {1:3, 2:6, 3:9},
        3: {1:3, 2:6, 3:9}}

    sfName = {0:"Terry Crews", 1:"Jason Statham", 2:"Wesley Sniper", 3:"Jet Ri", 4:"Steve Seagal",
                5:"Super Merio", 6:"Vin Dieser", 7:"Chack Norris", 8:"The Roch", 9:"Ernold Schwarzenegger",
                10:"Pariz Hilten", 11:"Jackie Chen", 12:"Steve Urkel", 13:"John Cena", 14:"James Bend",
                15:"Dexter", 16:"Agua Man", 17:"Bruce Hee"}

    sfDamage = {0:16, 1:18, 2:13, 3:20, 4:16, 5:15, 6:13, 7:32, 8:24, 9:26, 10:6, 11:9, 12:7, 13:26, 14:28, 15:13, 16:7, 17:29}

    global cardName
    global cardAttacks
    global cardStamina
    global sfName
    global sfDamage

    pygame.mixer.init(44100, -16,2,2048)

    try:
        pygame.mixer.music.load('music.wav') # Attempts to play music
        pygame.mixer.music.play(-1, 0.0)
    except:
        pass

    tilelist = {"": ""}
    tiles = 11
    numberOfPlayers = 4
    playerN = 0
    forward = 0
    playerColors = {0: (189,33,50), 1: (26,118,186), 2: (15,103,59), 3: (254,220,56)}
    pickedCards = {1: -1, 2: -1}
    pickedSFCard = -1
    activePlayers = numberOfPlayers
    bCurrentImage = 1
    music_playing = True
    ng = False
    global tilelist
    global tiles
    global numberOfPlayers
    global playerN
    global forward
    global playerColors
    global pickedCards
    global activePlayers
    global bCurrentImage
    global pickedSFCard
    global music_playing
    global ng

    global screen
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
        dice_rect = (screenX//2-(screenX//tiles//2), screenY//tiles, screenX//tiles, screenY//tiles)
        dice_button=screen.fill(players[playerN].Color, dice_rect)
        dice_text = font.render(str(forward), True, (255,255,255))
        dice = pygame.transform.scale(pygame.image.load('die.png'), (screenX//tiles, screenY//tiles))
        font = pygame.font.SysFont("Helvetica", 40)
        playerStat = font.render('Player: {0}' .format(players[playerN].Name), True, players[playerN].Color)
        healthStat = font.render('Health: {0}' .format(players[playerN].Health), True, players[playerN].Color)
        staminaStat = font.render('Stamina: {0}' .format(players[playerN].Stamina), True, players[playerN].Color)

        screen.blit(dice_text, ((screenX-(screenX//tiles+100)), screenY//tiles))
        screen.blit(dice, (screenX//2-(screenX//tiles//2),screenY//tiles))
        screen.blit(playerStat, (screenX//tiles, screenY//tiles+20))
        screen.blit(healthStat, (screenX//tiles, screenY//tiles+80))
        screen.blit(staminaStat, (screenX//tiles, screenY//tiles+140))

        pygame.event.get()
        (b1,b2,b3) = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        if dice_button.collidepoint(mpos) and b1 == 1:
            if players[playerN].Health < 1:
                players[playerN].Removed = True
            else:
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

connection.close()
main()





# sql_command ="""INSERT INTO player (Id) VALUES (1231313)"""
# cursor.execute(sql_command)
#
# connection.commit()

# cursor.execute("SELECT * FROM player")
# print("fetchall:")
# result = cursor.fetchall()
# for r in result:
#     print(r)
#
# connection.close()
