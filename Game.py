import sys
import pygame
from pygame.locals import *

def main():
    """ Set up the game and run the main loop """
    pygame.init()      # Prepare the pygame module for use
    surface_sz = 860,860  # Desired physical surface size, in pixels.
    screen = pygame.display.set_mode(surface_sz)
    # Create surface of (width, height), and its window.
    main_surface = pygame.display.set_mode((surface_sz))

    # Set up some data to describe a small rectangle and its color
    small_rect = (125, 125, 600, 600)    # (x, y, size x, size y)
    some_color = (255, 255, 255)            # A color is a mix of (Red, Green, Blue)

    test = 0

    while True:
        pygame.display.flip()
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop

        # Update your game objects and data structures here...

        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        main_surface.fill((0, 200, 255)) # fills background with blue



        my_font = pygame.font.SysFont("Arial", 16)    #creates font with font courier size 16
        the_text = my_font.render("test: {0}".format(test), True, (0,0,0))   # Text, AA , color
        screen.blit(the_text, (10, 10))     # draws text at 10,10
        test += 1       # increase test value

        # Instantiate 16 point Courier font to draw text.

        # Overpaint a smaller rectangle on the main surface
        main_surface.fill(some_color, small_rect)

        my_clock = pygame.time.Clock()
        my_clock.tick(60)

        # Now the surface is ready, tell pygame to display it!


    pygame.quit()     # Once we leave the loop, close the window.

main()