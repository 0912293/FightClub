import sys
import pygame
from pygame.locals import *

class Tile:
    def __init__(self, id, type, first, positionX, positionY):
        self.Id = id
        self.Type = type
        self.First = first
        self.PositionX = positionX
        self.PositionY = positionY

def drawBoard(tid, max):
    if tid == 0:
        ttype = "Regular"
        first = True
        positionX = 0
        positionY = 0
    else:
        ttype = "Regular"
        first = False
        positionX = positionX + 300
        positionY
    global positionX
    global positionY
    if tid < max:
        return Tile(tid, ttype, first, positionX, positionY), drawBoard(tid+1, max)
    else:
        return Tile(tid, ttype, first, positionX, positionY)

def createBoard(tiles, screenY, screenX, main_surface):
    for i in range(tiles):
        for j in range(tiles):
            tile = ((tiles//screenX)*j, (tiles//screenY)*j, screenX//tiles, screenY//tiles)
            print("tile:", i, j, screenX//tiles*j, screenY//tiles*i)
            pygame.draw.rect(main_surface,(255, 0, 255),(screenX//tiles*j, screenY//tiles*i, screenX//tiles, screenY//tiles), 5)
            # pygame.display.set_mode((screenX, screenY)).fill((255, 0, 255), tile) 

# tilelist = Tile(0, True, "Regular", 0, 0)
# tilelist = drawBoard(0, 4)
# print(type(tilelist), tilelist.Id)

def main():
    """ Set up the game and run the main loop """
    pygame.init()      # Prepare the pygame module for use
    pygame.display.set_caption('Fightclub')
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
    # Set up some data to describe a small rectangle and its color
    small_rect = (100, 100, screenX-200, screenY-200)    # (x, y, size x, size y)
    some_color = (255, 255, 255)            # A color is a mix of (Red, Green, Blue)
    # tilelist = [drawBoard(0)]
    # print(tilelist.Id, tilelist.Type, tilelist.PositionX, tilelist.PositionY)

    while True:
        pygame.display.flip()
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT or pygame.key.get_pressed()[27] == 1:
            break
        main_surface.fill((0, 200, 255))
        createBoard(11, screenY, screenX, main_surface)

        my_font = pygame.font.SysFont("Arial", 16)
        the_text = my_font.render("test: {0}".format("Hello World"), True, (0,0,0))   # Text, AA , color
        screen.blit(the_text, (10, 10))     # draws text at 10,10
        test += 1
        # main_surface.fill(some_color, small_rect)

        my_clock = pygame.time.Clock()
        my_clock.tick(60)


    pygame.quit()     # Once we leave the loop, close the window.

main()