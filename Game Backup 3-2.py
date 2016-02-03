import sys
import pygame
from pygame.locals import *
import sqlite3
import os
import random
import pickle
from time import *

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
database = 'database.db'
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
    cursor = connection.cursor()

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
    center = pygame.transform.scale(pygame.image.load('boxing_ring_logo.png'), (screenX-(screenX//tiles*2), screenY-(screenY//tiles*2)-2))
    screen.blit(center, (screenX//tiles, screenY//tiles))
    global numberOfBoardRefreshes
    for i in range(tiles):
        for j in range(tiles):
            if numberOfBoardRefreshes == 0:
                pygame.display.flip()
            tile = (screenX//tiles*j, screenY//tiles*i, screenX//tiles, screenY//tiles)
            if i == 0 or j == 0 or i == tiles-1 or j == tiles-1:
                if (i == 0 and j == 0) or (i == 0 and j == 1) or (i == 1 and j == 0):
                    try:
                        pygame.draw.rect(screen, players[0].Color, tile)
                        pygame.draw.rect(screen, grey, tile, 10)
                    except:
                        pygame.draw.rect(screen, grey, tile, 10)
                elif (i == tiles-1 and j == 0) or (i == tiles-1 and j == 1) or (i == tiles-2 and j == 0):
                    try:
                        pygame.draw.rect(screen, players[1].Color, tile)
                        pygame.draw.rect(screen, grey, tile, 10)
                    except:
                        pygame.draw.rect(screen, grey, tile, 10)
                elif (i == 0 and j == tiles-1) or (i == 0 and j == tiles-2) or (i == 1 and j == tiles-1):
                    try:
                        pygame.draw.rect(screen, players[3].Color, tile)
                        pygame.draw.rect(screen, grey, tile, 10)
                    except:
                        pygame.draw.rect(screen, grey,tile, 10)
                elif (i == tiles-1 and j == tiles-1) or (i == tiles-1 and j == tiles-2) or (i == tiles-2 and j == tiles-1):
                    try:
                        pygame.draw.rect(screen, players[2].Color, tile)
                        pygame.draw.rect(screen, grey, tile, 10)
                    except:
                        pygame.draw.rect(screen, grey,tile, 10)
                elif (i == 0 and j == tiles//2) or (i == tiles//2 and j == tiles-1) or (i == tiles-1 and j == tiles//2) or (i == tiles//2 and j == 0):
                    pygame.draw.rect(screen, red, tile, 10)
                    screen.blit(superfightImg, tile)
                else:
                    pygame.draw.rect(screen, grey,tile, 10)
    numberOfBoardRefreshes += 1
    print("Board has been resfreshed ", numberOfBoardRefreshes, "times.")

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
    global bCurrentImage
    global music_playing
    global players
    global ingame

    animationImg = pygame.transform.scale(pygame.image.load(os.path.join("anime", "an" + str(bCurrentImage) + ".png")), (screenX, screenY))
    screen.blit(animationImg, (0,0))
    if bCurrentImage < 9:
        bCurrentImage += 1
    else:
        bCurrentImage = 1

    my_font = pygame.font.SysFont("Arial", 70)
    if ng:
        start_button = Rect(0, 150, screenX//2, 75)
        startB_img = pygame.transform.scale(pygame.image.load('b_continue.png'), (screenX//3, 75))
        screen.blit(startB_img,(0, 150))

    if os.path.isfile("database.db"):
        load_button = Rect(0, 450, screenX//2.5, 75)
        loadB_img = pygame.transform.scale(pygame.image.load('b_load.png'), (screenX//6, 75))
        screen.blit(loadB_img,(0, 450))

    if ingame:
        save_button = Rect(0, 350, screenX//2.5, 75)
        saveB_img = pygame.transform.scale(pygame.image.load('b_save.png'), (screenX//6, 75))
        screen.blit(saveB_img,(0, 350))

    #buttons (x, y, size x, size y)
    new_button = Rect(0, 50, screenX//2.5, 75)
    instruct_button = Rect(0, 250, screenX//2.5, 75)
    settings_button = Rect(0, 550, screenX//2.5, 75)
    exit_button = Rect(0, 650, screenX//2.5, 75)

    #images
    newgameB_img = pygame.transform.scale(pygame.image.load('b_newgame.png'), (screenX//3, 75))
    manualB_img = pygame.transform.scale(pygame.image.load('b_manual.png'), (screenX//4, 75))
    settingsB_img = pygame.transform.scale(pygame.image.load('b_settings.png'), (screenX//4, 75))
    exitB_img = pygame.transform.scale(pygame.image.load('b_exit.png'), (screenX//6, 75))
    
    #draw images
    screen.blit(newgameB_img,(0, 50))
    screen.blit(manualB_img,(0, 250))
    screen.blit(settingsB_img,(0,535))
    screen.blit(exitB_img, (0, 620))

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if new_button.collidepoint(mpos) & b1==1:
        return newGame()
    if ng:
        if start_button.collidepoint(mpos) and b1==1:
            return
    if instruct_button.collidepoint(mpos) & b1==1:
        instructions()
    if ingame:
        if save_button.collidepoint(mpos) & b1==1:
            connection = sqlite3.connect(database)  #-- connection to database
            cursor = connection.cursor()
            cursor.execute('DROP TABLE IF EXISTS player')       #-------drops table, creates new
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
            for s in range(0,numberOfPlayers):
                R, G, B = players[s].Color      #-------- adds data in the table
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
                data1.append(B)
            it = [iter(data1)] * 12         #--------- creates list of tuples
            data=list(zip(*it))
            print(data)

            cursor.executemany('INSERT INTO player VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',data)      #-------------inserts data
            connection.commit()                   #------- commits it
            cursor.execute("SELECT * FROM player")      #---prints all data in database
            print("fetchall:")
            result = cursor.fetchall()
            for r in result:
                print(r)
            print(data1)
            print("Saved!")

    if os.path.isfile("database.db"):
        if load_button.collidepoint(mpos) & b1==1:
            connection = sqlite3.connect(database)  #-- connection to database
            cursor = connection.cursor()
            createList(0,0,0)
            playerCreate()
            ingame = True
            for s in range(0,numberOfPlayers):        #id, sprite, position, x, y, health, stamina, name, color, removed):
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
                players[s].Color = (r,g,b)
                global players
                global music_playing
            print("Loaded!")
            ng = True
            global ng
            return

    if settings_button.collidepoint(mpos) and b1==1:
        settings()
    if exit_button.collidepoint(mpos) and b1==1:
        pygame.quit()
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    return menu()

def music_play(n):
    music=['music3.wav','sound_effects/fight_bell.wav','sound_effects/button2.wav']
    pygame.mixer.music.load(music[n])
    if music_playing:
        if n == 0:
            pygame.mixer.music.play(-1, 0.0)
        else:
            pygame.mixer.music.play(0, 0.0)

def newGame():
    ng = False
    pygame.display.flip()
    black = (0, 0, 0)
    red = (150, 0, 0)
    screen.fill(red)
    logotexture = pygame.transform.scale(pygame.image.load('boxing_ring.png'), (screenX, screenY))
    screen.blit(logotexture, (0,0))
    playerToPickCard = 0
    x = True
    y = True
    i = True
    j = True
    global playerToPickCard
    global x
    global y
    global i
    global j
    global ng
    global music_playing
    global numberOfPlayers

    #buttons (x, y, size x, size y)
    start_button = Rect(0, 150, screenX//2.5, 75)
    p_button = Rect(0, 250, screenX//2.5, 75)
    return_button = Rect(0, screenY-(screenY//tiles), screenX//2.5, 75)

    #text Text, AA , color
    my_font = pygame.font.SysFont("Arial", 70)
    startB_img = pygame.transform.scale(pygame.image.load('b_next.png'), (screenX//5, 75))
    pB_img = pygame.transform.scale(pygame.image.load('b_players' + str(numberOfPlayers) + ".png"), (screenX//3, 75))
    returnB_img = pygame.transform.scale(pygame.image.load('b_return.png'), (screenX//4, 75))

    #draw text
    screen.blit(startB_img,(0, 150))
    screen.blit(pB_img,(0, 250))
    screen.blit(returnB_img, (0, screenY-(screenY//tiles)))

    cpuImg = pygame.transform.scale(pygame.image.load('b_computerplayers.png'), (screenX//2, 100))
    screen.blit(cpuImg, (0, screenY//2))

    for s in range(numberOfPlayers):
        cpuButton = Rect((screenX//tiles+50)*s, screenY//2+75, 165, 75)
        cpuButtonImg = pygame.transform.scale(pygame.image.load(os.path.join("b_player" + str(s+1) + ".png")), (screenX//8, 75))
        if s in computerPlayers:
            screen.fill((0,0,100), cpuButton)
        else:
            screen.fill((0,0,0), cpuButton)
        screen.blit(cpuButtonImg,((screenX//tiles+50)*s, screenY//2+75))

        (b1,b2,b3) = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        if cpuButton.collidepoint(mpos) and b1==1:
            if s in computerPlayers:
                computerPlayers.remove(s)
            else:
                computerPlayers.append(s)

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if start_button.collidepoint(mpos) and b1==1:
        createList(0,0,0)
        playerCreate()
        chooseCardScreen()
    if p_button.collidepoint(mpos) and b1==1:
        if numberOfPlayers < 4:
            numberOfPlayers += 1
        else:
            numberOfPlayers = 2
    if return_button.collidepoint(mpos) and b1==1:
        return menu()
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
    bCurrentImage = 1
    pygame.image.load(os.path.join("player_cards", "p" +str(bCurrentImage) + ".png"))
    if bCurrentImage < 4:
        bCurrentImage += 1
    else:
        bCurrentImage =1
    global playerToPickCard
    global x
    global y
    global i
    global j
    global ng
    global music_playing
    global numberOfPlayers

    #buttons (x, y, size x, size y)
    start_button = Rect(0,50,screenX//2.5, 75)
    return_button = Rect(0, screenY-(screenY//tiles), screenX//2.5, 75)
    if x:
        img1_button = pygame.draw.rect(screen, black, [400,250,300,200])
    if y:
        img2_button = pygame.draw.rect(screen, black, [800,250,300,200])
    if i:
        img3_button = pygame.draw.rect(screen, black, [400,500,300,200])
    if j:
        img4_button = pygame.draw.rect(screen, black, [800,500,300,200])

    startB_img = pygame.transform.scale(pygame.image.load('b_start.png'), (screenX//5, 75))
    returnB_img = pygame.transform.scale(pygame.image.load('b_return.png'), (screenX//4, 75))
    chooseC_img = pygame.transform.scale(pygame.image.load('b_choosechar.png'), (screenX//2, 75))

    for s in range(4):
        currentPlayer_img = pygame.transform.scale(pygame.image.load(os.path.join("b_player" + str(playerToPickCard+1) + ".png")), (screenX//3, 100))
        cardsImage = pygame.transform.scale(pygame.image.load(os.path.join("player_cards", "p" + str(s+1) + ".png")),(300,200))
        if s == 0 and x:
            screen.blit(cardsImage, (400, 250))
        if s == 1 and y:
            screen.blit(cardsImage, (800, 250))
        if s == 2 and i:
            screen.blit(cardsImage, (400, 500))
        if s == 3 and j:
            screen.blit(cardsImage, (800, 500))

        #button actions
        pygame.event.get()
        (b1,b2,b3) = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        if x and img1_button.collidepoint(mpos) and b1==1:
            players[playerToPickCard].Card = 1
            players[playerToPickCard].Name = cardName[0]
            playerToPickCard += 1
            x = False
        if y and img2_button.collidepoint(mpos) and b1==1:
            players[playerToPickCard].Card = 2
            players[playerToPickCard].Name = cardName[1]
            playerToPickCard += 1
            y = False
        if i and img3_button.collidepoint(mpos) and b1==1:
            players[playerToPickCard].Card = 3
            players[playerToPickCard].Name = cardName[2]
            playerToPickCard += 1
            i = False
        if j and img4_button.collidepoint(mpos) and b1==1:
            players[playerToPickCard].Card = 4
            players[playerToPickCard].Name = cardName[3]
            playerToPickCard += 1
            j = False
        global players
        if playerToPickCard >= numberOfPlayers:
            ng = True
            global players
            return

    #draw text
    screen.blit(chooseC_img, (450, 50))
    screen.blit(currentPlayer_img, (450, 150))
    screen.blit(startB_img,(0, 50))
    screen.blit(returnB_img, (0, screenY-(screenY//tiles)))

    if start_button.collidepoint(mpos) and b1==1:
        ng = True
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
    return_img = pygame.transform.scale(pygame.image.load('b_return.png'), (screenX//4, 75))
    screen.blit(return_img, (screenX//2-(len("RETURN")*20), screenY-75))

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
    black = (0, 0, 0)
    red = (150, 0, 0)
    data2 = []
    screen.fill(red)
    logotexture = pygame.transform.scale(pygame.image.load('boxing_ring_logo.png'), (screenX, screenY))
    screen.blit(logotexture, (0,0))
    global music_playing

    #buttons (x, y, size x, size y)
    mute_button = Rect(screenX-screenX//2.5, 50,screenX//2.5, 75)
    return_button = Rect(screenX-screenX//2.5, 550, screenX//2.5, 75)

    if music_playing:
        muteB_img = pygame.transform.scale(pygame.image.load('b_unmute.png'), (screenX//12, 75))
    else:
        muteB_img = pygame.transform.scale(pygame.image.load('b_mute.png'), (screenX//12, 75))
    returnB_img = pygame.transform.scale(pygame.image.load('b_return.png'), (screenX//4, 75))

    #draw text
    screen.blit(muteB_img,(screenX-screenX//2.5, 50))
    screen.blit(returnB_img, (screenX-screenX//2.5, 550))
    pygame.display.flip()

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if mute_button.collidepoint(mpos) and b1==1:
        if music_playing:
            music_playing = False
        else:
            music_playing = True
        print(music_playing)
        music_play(0)
        data2.append(music_playing)
        with open('savefile', 'wb') as f:
            pickle.dump(data2, f)
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
        players[s] = Player(s, pygame.transform.scale(pygame.image.load(os.path.join("pawns", "pawn" + str(s+1) + "-8bit.png")), (screenX//tiles-10, screenY//tiles-10)).convert_alpha(), tilelist[(tiles-1)*s].Id, tilelist[(tiles-1)*s].X*(screenX//tiles)+5, tilelist[(tiles-1)*s].Y*(screenY//tiles)+5, 100, 15, -1, playerColors, False, cardName[s])
    global players

def playerMove(s, forward):
    if players[s].Position + forward > len(tilelist)-2:
        remainder = players[s].Position + forward - len(tilelist)-1
        players[s].Position = remainder
    players[s].Position += 1
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
    if player == numberOfPlayers-1:
        playerMove(player, forward)
        checkFight(player)
        playerN = 0
    elif player < numberOfPlayers-1:
        playerMove(player, forward)
        checkFight(player)
        playerN += 1

def checkFight(player):
    for s in range(4):
            print("Player:", s, "with card", players[s].Card)
    for s in range(len(tilelist)-1):
        dice1 = random.randint(1,6)
        dicelist = [dice1, random.randint(1,6)]
        if players[player].Position == tilelist[s].Id and tilelist[s].Type == "superfight":
            diceRoll(player, -1, -1, -1, False)
            music_play(1)
            superFight(player, random.randint(1,17), dice1)
            music_play(0)
            return
        elif players[player].Position == tilelist[s].Id and tilelist[s].Type == "corner" and player == tilelist[s].Owner:
            players[player].Stamina = 15
            break
        elif players[player].Position == tilelist[s].Id and tilelist[s].Type == "corner" and player != tilelist[s].Owner and not players[tilelist[s].Owner].Removed:
            music_play(1)
            diceRoll(player, s, -1, -1, True)
            fight(player, s, True, dicelist)
            music_play(0)
            return
        else:
            for s in range(len(players)-1):
                if (players[player].Position == players[s].Position and players[player].Id != players[s].Id):
                    music_play(1)
                    diceRoll(player, s, -1, -1, False)
                    fight(player, s, False, dicelist)
                    music_play(0)
                    return

def diceRoll(attacker, defender, dice1, dice2, tile):
    if defender < 0:
        background = players[attacker].Color
        background_rect = (0, 0, screenX, screenY)
        screen.fill(background, background_rect)
    else:
        left_side = players[attacker].Color
        left_rect = (0, 0, screenX//2, screenY)
        if tile:
            print(defender)
            right_side = players[tilelist[defender].Owner].Color
        else:
            right_side = players[defender].Color
        right_rect = (screenX//2, 0, screenX//2, screenY)
        screen.fill(left_side, left_rect)
        screen.fill(right_side, right_rect)
        dice2_rect = Rect(screenX//4*3, screenY//2, screenX//tiles, screenY//tiles)
        dice_button2 = screen.fill(right_side, dice2_rect)
        screen.blit(dice, (screenX//4*3,screenY//2))

    font = pygame.font.SysFont("Helvetica", 70)
    rolldice_text = font.render("Roll the dice!", True, (255,255,255))
    dice1_rect = Rect(screenX//4, screenY//2, screenX//tiles, screenY//tiles)
    dice_button1 = screen.fill(players[attacker].Color, dice1_rect)
    screen.blit(dice, (screenX//4,screenY//2))
    screen.blit(rolldice_text, (screenX//3, screenY//tiles))
    pygame.display.flip()

    if dice1 == -1:
        if attacker in computerPlayers:
            dice1 = random.randint(1,6)
            if dice2 != -1 or defender <= 0:
                return
    if dice2 == -1:
        if tile:
            defender = tilelist[defender].Owner
        if defender in computerPlayers:
            dice2 = random.randint(1,6)
            if dice1 != -1:
                return

    pygame.event.get()
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if defender >= 0 and dice_button2.collidepoint(mpos) and b1 == 1:
        dice2 = random.randint(1,6)
    if dice_button1.collidepoint(mpos) and b1 == 1:
        dice1 = random.randint(1,6)
        if defender <= 0:
            return
    if dice1 != -1 and dice2 != -1:
        return
    if pygame.key.get_pressed()[27] == 1:
        menu()
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    diceRoll(attacker, defender, dice1, dice2, tile)

def superFight(player, superfighter, dice):
    screen.fill((0,0,0))
    global players
    for s in range(4):
        print("Player:", s, "with card", players[s].Card)
    card1 = pygame.transform.scale(pygame.image.load(os.path.join("player_cards", "p" + str(players[player].Card) + ".png")), (screenX//3, screenY//3))
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
        cardDamageText = "Damage: " + str(cardAttacks[player][s+1]*dice)
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
    pygame.display.flip()

    pygame.event.get()
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if player in computerPlayers:
        pickedSFCard = random.randint(1,3)
        music_play(2)
    else:
        for s in range(len(cardAttacks[s])):
            if choice_button[1][s].collidepoint(mpos) and b1 == 1:
                pickedSFCard = s+1
                music_play(2)

    if pickedSFCard != -1:
        superFightResult(player, superfighter, pickedSFCard, dice)
        return
    if pygame.key.get_pressed()[27] == 1:
        menu()
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    superFight(player, superfighter, dice)

def fight(player, defender, tile, dicelist):
    print(defender)
    screen.fill((0, 0, 0))
    card1 = pygame.transform.scale(pygame.image.load(os.path.join("player_cards", "p" + str(players[player].Card) + ".png")), (screenX//3, screenY//3))
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
            if pickedCards[i+1] == s+1:
                cardcolor = (100, 0, 0)
            else:
                cardcolor = (0, 0, 0)
            font = pygame.font.SysFont("Helvetica", 45)
            cardNameText = "Attack " + str(s+1)
            name_text = font.render(cardNameText, True, (255,255,255))

            font = pygame.font.SysFont("Helvetica", 14)
            cardDamageText = "Damage: " + str(cardAttacks[p][s+1]*dicelist[i])
            cardStaminaText = "Required Stamina: " + str(cardStamina[p][s+1])
            damage_text = font.render(cardDamageText, True, (255,255,255))
            stamina_text = font.render(cardStaminaText, True, (255,255,255))
            choice_rect = Rect(100+(screenX//2)*i+1, (screenY//2)+100*s, screenX//5, 75)
            choice_button[i+1].append(screen.fill(cardcolor, choice_rect))

            screen.blit(name_text, (110+(screenX//2)*i+1, (screenY//2)+100*s))
            screen.blit(damage_text, (120+(screenX//2)*i+1, (screenY//2)+45+100*s))
            screen.blit(stamina_text, (120+(screenX//2)*i+1, (screenY//2)+60+100*s))

    font = pygame.font.SysFont("Helvetica", 70)
    versus_text = font.render("VS", True, (255,255,255))
    screen.blit(versus_text, (screenX//2-(len("VS")*25), 100))
    screen.blit(card1, ((screenX//tiles), screenY//tiles))
    screen.blit(card2, ((screenX//2+screenX//tiles, screenY//tiles)))
    pygame.display.flip()

    pygame.event.get()
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    for i in range(2):
        if tile:
            defender2 = tilelist[defender].Owner
        else:
            defender2 = defender
        if i == 0 and player in computerPlayers:
            pickedCards[i+1] = random.randint(1,3)
            music_play(2)
        elif i == 1 and defender2 in computerPlayers:
            pickedCards[i+1] = random.randint(1,3)
            music_play(2)
        else:
            for s in range(len(cardAttacks[s])):
                if choice_button[i+1][s].collidepoint(mpos) and b1 == 1:
                    pickedCards[i+1] = s+1
                    music_play(2)

    if pickedCards[1] != -1 and pickedCards[2] != -1 and tile:
        fightResult(player, players[tilelist[defender].Owner].Id, pickedCards[1], pickedCards[2], tile, dicelist)
        return
    elif pickedCards[1] != -1 and pickedCards[2] != -1 and not tile:
        fightResult(player, defender, pickedCards[1], pickedCards[2], tile, dicelist)
        return
    if pygame.key.get_pressed()[27] == 1:
        menu()
    if pygame.key.get_pressed()[113] == 1:
        pygame.quit()
    pygame.event.wait()
    fight(player, defender, tile, dicelist)

def superFightResult(player, defender, pickedCard, dice):
    if not players[player].Stamina - cardStamina[player][pickedCard] < 0:
        if cardAttacks[player][pickedCard]*dice < sfDamage[defender]:
            players[player].Health -= sfDamage[defender]
            players[player].Stamina -= cardStamina[player][pickedCard]
        else:
            players[player].Stamina -= cardStamina[player][pickedCard]
    else:
        players[player].Health -= sfDamage[defender]
    global players
    checkHealth()
    return
            
def fightResult(attacker, defender, attackerCard, defenderCard, tile, dicelist):
    if not players[attacker].Stamina - cardStamina[attacker][attackerCard] < 0:
        players[defender].Health -= cardAttacks[attacker][attackerCard]*dicelist[0]
        players[attacker].Stamina -= cardStamina[attacker][attackerCard]
    if not players[defender].Stamina - cardStamina[defender][defenderCard] < 0:
        players[attacker].Health -= cardAttacks[defender][defenderCard]*dicelist[1]
        players[defender].Stamina -= cardStamina[defender][defenderCard]
    global players
    checkHealth()
    return

def checkHealth():
    playersHealthList = {}
    activePlayers = numberOfPlayers
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
            winner_text = font.render("Player {0} won!" .format(winner+1), True, players[winner].Color)
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

    cardAttacks = {0: {1:4, 2:6, 3:10},
        1: {1:4, 2:7, 3:9},
        2: {1:3, 2:7, 3:10},
        3: {1:3, 2:6, 3:11}}

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
    ingame = False
    computerPlayers = []
    numberOfBoardRefreshes = 0

    pygame.mixer.init(44100, -16,2,2048)
    if os.path.isfile("savefile"):
        with open('savefile', 'rb') as f:
            data2 = pickle.load(f)
            music_playing = data2[0]
    music_play(0)

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
    global ingame
    global computerPlayers
    global numberOfBoardRefreshes

    global screen
    menu()
    ingame = True

    while True:
        pygame.display.flip()
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
        screen.fill((0, 0, 0))
        createBoard()

        if not players[playerN].Health < 1:
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

            global dice
            global dice_rect

            screen.blit(dice_text, ((screenX-(screenX//tiles+100)), screenY//tiles))
            screen.blit(dice, (screenX//2-(screenX//tiles//2),screenY//tiles))
            screen.blit(playerStat, (screenX//tiles+20, screenY//tiles+20))
            screen.blit(healthStat, (screenX//tiles+20, screenY//tiles+80))
            screen.blit(staminaStat, (screenX//tiles+20, screenY//tiles+140))

            pygame.event.get()
            (b1,b2,b3) = pygame.mouse.get_pressed()
            mpos = pygame.mouse.get_pos()
            if playerN in computerPlayers:
                print("computerTurn!")
                turn(playerN)
            elif dice_button.collidepoint(mpos) and b1 == 1:
                turn(playerN)

            data1 = []
            for s in range(numberOfPlayers):
                if not players[s].Removed:
                    screen.blit(players[s].Sprite, (players[s].X, players[s].Y))
        else:
            players[playerN].Removed = True
            if playerN == numberOfPlayers - 1:
                playerN = 0
            elif playerN < numberOfPlayers-1:
                playerN += 1
        checkHealth()

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