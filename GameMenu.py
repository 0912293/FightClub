import sys
import pygame
from pygame.locals import *
import time
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def manual(main_surface,instructions_0,instructions_1):
    pygame.display.flip()
    main_surface.fill((0, 0, 0))
    main_surface.blit(instructions_0,(80, 80))
    main_surface.blit(instructions_1,(80, 120))
    if pygame.key.get_pressed()[27] == 1:
        return
    pygame.event.wait()
    return manual(main_surface,instructions_0,instructions_1)

def main():
    """ Set up the game and run the main loop """
    pygame.init()      # Prepare the pygame module for use
    pygame.display.set_caption('Fightclub') # Titel bovenaan de venster

    try:
        pygame.mixer.music.load('beep.mp3') # muziek
        pygame.mixer.music.play(-1, 0.0)
    except:
        pass

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
    start_rect = (screenX-screenX / 2 - 250, screenY-screenY /2-160, 500, 75)
    instruct_rect = (screenX-screenX / 2 - 250, screenY-screenY /2-80, 500, 75)
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
        instruct_button=screen.fill(some_color, instruct_rect)

        #----text----#
        my_font = pygame.font.SysFont("Arial", 60)
        txt_font = pygame.font.SysFont("Arial", 30)
        startB_text = my_font.render('START', True, (255,255,255))
        instructB_text = my_font.render('INSTRUCTIONS', True, (255,255,255))
        exitB_text = my_font.render("EXIT", True, (255,255,255))   # Text, AA , color
        screen.blit(startB_text,(screenX-screenX / 2 - 115,screenY-screenY /2-160))
        screen.blit(instructB_text,(screenX-screenX / 2 -225,screenY-screenY /2-80))
        screen.blit(exitB_text, (screenX-screenX / 2 - 80, screenY-screenY /2))     # draws text at 10,10

        instructions_0 = txt_font.render("1.Press the escape key to open the menu", True, (255,255,255))
        instructions_1 = txt_font.render("2.To move your pawn press the die button", True, (255,255,255))
        #----text end---#



        #----buttons----#
        (b1,b2,b3) = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        if exit_button.collidepoint(mpos) & b1==1:
            break                   #exits game
        if instruct_button.collidepoint(mpos) & b1==1:
            manual(main_surface,instructions_0,instructions_1)

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


