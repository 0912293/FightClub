import sys
import pygame
from pygame.locals import *
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def createBoard(main_surface):
    tilelist = []
    for i in range(tiles):
        for j in range(tiles):
            tile = (screenX//tiles*j, screenY//tiles*i, screenX//tiles, screenY//tiles)
            if i == 0 or j == 0 or i == tiles-1 or j == tiles-1:
                color = (0, 200, 255)
                width = 10
                if (i == 0 and j == 0) or (i == tiles-1 and j == 0) or (i == 0 and j == tiles-1) or (i == tiles-1 and j == tiles-1):
                    pygame.draw.rect(main_surface,(0,255,0),tile)
                else:
                    pygame.draw.rect(main_surface,(0,200,255),tile, 10)
            else:
                pygame.draw.rect(main_surface,(0, 0, 0),tile)
    center = pygame.transform.scale(pygame.image.load('BoardCenter.png'), (screenX-(screenX//tiles*2), screenY-(screenY//tiles*2)))
    main_surface.blit(center, (screenX//tiles,screenY//tiles))

def menu(main_surface):
    pygame.display.flip()
    black = (0, 0, 0)
    main_surface.fill(black)
    logotexture = pygame.transform.scale(pygame.image.load('logo_super.png'), (screenX, screenY))
    main_surface.blit(logotexture, (0,0))

    #buttons
    exit_rect = (screenX-screenX / 2 - 250, screenY-screenY /2, 500, 75)    # (x, y, size x, size y)
    start_rect = (screenX-screenX / 2 - 250, screenY-screenY /2-80, 500, 75)
    start_button=main_surface.fill(black, start_rect)
    exit_button=main_surface.fill(black, exit_rect)

    #text
    my_font = pygame.font.SysFont("Arial", 70)
    startB_text = my_font.render('START', True, (255,255,255))
    exitB_text = my_font.render("EXIT", True, (255,255,255))   # Text, AA , color
    main_surface.blit(startB_text,(screenX-screenX / 2 - 115,screenY-screenY /2-80))
    main_surface.blit(exitB_text, (screenX-screenX / 2 - 80, screenY-screenY /2))     # draws text at 10,10

    #button actions
    (b1,b2,b3) = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    if start_button.collidepoint(mpos) and b1==1:
        return
    if exit_button.collidepoint(mpos) & b1==1:
        pygame.quit()
    pygame.event.wait()
    menu(main_surface)

def main():
    pygame.init()      # Prepare the pygame module for use
    pygame.display.set_caption('Fightclub')

    try:
        pygame.mixer.music.load('beep.mp3') # muziek
        pygame.mixer.music.play(-1, 0.0)
    except:
        pass

    tiles = 11
    global tiles
    if pygame.display.list_modes()[0] == (2880, 1800) or pygame.display.list_modes()[0] == (2560, 1600):
    	HDPI = 2
    	screenX, screenY = pygame.display.list_modes()[0]
    	screenX = screenX//HDPI
    	screenY = screenY//HDPI
    	screen = pygame.display.set_mode((screenX, screenY))
    else:
    	screenX, screenY = pygame.display.list_modes()[0]
    screenX -= 100
    screenY -= 100
    global screenX
    global screenY
    screen = pygame.display.set_mode((screenX, screenY))
    main_surface = screen

    while True:
        pygame.display.flip()
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
        main_surface.fill((255, 255, 255))
        createBoard(main_surface)

        my_font = pygame.font.SysFont("Arial", 16)
        the_text = my_font.render("test: {0}".format("Hello World"), True, (0,0,0))   # Text, AA , color
        screen.blit(the_text, (10, 10))     # draws text at 10,10
        if pygame.key.get_pressed()[27] == 1:
            menu(main_surface)
        my_clock = pygame.time.Clock()
        my_clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()     # Once we leave the loop, close the window.

main()