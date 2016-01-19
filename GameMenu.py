import pygame

pygame.init()

class GameMenu():
    def __init__(self, screen, bg_color=(0,0,0)):

        self.screen = screen
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

    def run(self):
        mainloop = True

        small_rect = (220, 125, 200, 75)    # (x, y, size x, size y)
        some_color = ( 255, 255, 255)            # A color is a mix of (Red, Green, Blue)


        while mainloop:
            pygame.display.flip()
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

            # Redraw the background
            self.screen.fill(self.bg_color)

            rect=screen.fill(some_color, small_rect)

            my_font = pygame.font.SysFont("Arial", 70)
            the_text = my_font.render("EXIT", True, (0,0,0))   # Text, AA , color
            screen.blit(the_text, (220,125))     # draws text at 10,10

            #----button----#
            (b1,b2,b3) = pygame.mouse.get_pressed()
            mpos = pygame.mouse.get_pos()

            if rect.collidepoint(mpos) & b1==1:
                break                   #exits game
            #----button end----#


if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((860, 640), 0, 32)
    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen)
    gm.run()