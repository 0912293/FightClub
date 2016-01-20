import sys
import pygame
from pygame.locals import *
import time
import pygame.gfxdraw

def main():
    """ Set up the game and run the main loop """
    pygame.init()      # Prepare the pygame module for use
    pygame.display.set_caption('Fightclub') # Titel bovenaan de venster

    pygame.mixer.music.load('beep.mp3')   # muziek
    pygame.mixer.music.play(-1, 0.0)      # -1 loops 0.0 = ?

    if pygame.display.list_modes()[0] == (2880, 1800) or pygame.display.list_modes()[0] == (2560, 1600):
    	HDPI = 2
    	screenX, screenY = pygame.display.list_modes()[0]
    	screenX = screenX//HDPI
    	screenY = screenY//HDPI
    	screen = pygame.display.set_mode((screenX, screenY))
    else:
    	screenX, screenY = pygame.display.list_modes()[0]
    	screen = pygame.display.set_mode(pygame.display.list_modes()[0])
    # pygame.display.toggle_fullscreen()
    # Create surface of (width, height), and its window.
    main_surface = screen
    background = pygame.image.load('logo_super.png')
    exit_rect = (screenX-screenX / 2 - 250, screenY-screenY /2, 500, 75)    # (x, y, size x, size y)
    start_rect = (screenX-screenX / 2 - 250, screenY-screenY /2-80, 500, 75)
    some_color = ( 0, 0, 0)            # A color is a mix of (Red, Green, Blue)


    test = 0

    while True:
        pygame.display.flip()
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT or pygame.key.get_pressed()[27] == 1:
            break
        main_surface.fill((0, 0, 0))
        main_surface.blit(background,(screenX-screenX/2 - 750, -200))
        start_button=screen.fill(some_color, start_rect)
        exit_button=screen.fill(some_color, exit_rect)

        #----text----#
        my_font = pygame.font.SysFont("Arial", 70)
        startB_text = my_font.render('START', True, (255,255,255))
        exitB_text = my_font.render("EXIT", True, (255,255,255))   # Text, AA , color
        screen.blit(startB_text,(screenX-screenX / 2 - 115,screenY-screenY /2-80))
        screen.blit(exitB_text, (screenX-screenX / 2 - 80, screenY-screenY /2))     # draws text at 10,10
        #----text end---#


        #----buttons----#
        (b1,b2,b3) = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        if exit_button.collidepoint(mpos) & b1==1:
            break                   #exits game

        if start_button.collidepoint(mpos) & b1==1:
            print('start')
        #----buttons end----#

        my_clock = pygame.time.Clock()
        my_clock.tick(60)

    pygame.mixer.music.stop()

    pygame.quit()     # Once we leave the loop, close the window.

def createBoard():
	pass

main()