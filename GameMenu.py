import pygame

pygame.init()

class GameMenu():
    def __init__(self, screen, bg_color=(58,110,165)):

        self.screen = screen
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

    def run(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

            # Redraw the background
            self.screen.fill(self.bg_color)
            pygame.display.flip()

if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen)
    gm.run()