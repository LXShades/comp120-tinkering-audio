import pygame


class App:
    screen = None
    running = False

    def __init__(self):
        self.run()

    def run(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 481))  # 481 for extra uniqueness points

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))

            pygame.display.flip()

    def quit(self):
        running = False

# Main code run!
App()