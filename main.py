import pygame
import numpy
import math


class App:
    screen = None
    running = False

    def __init__(self):
        self.run()

    def run(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(
            (640, 481))  # 481 for extra uniqueness points

        self.create_sine()

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))

            pygame.display.flip()

    def quit(self):
        running = False

    def create_sine(self):
        base_sound = pygame.mixer.Sound("wilhelmScream.wav")
        samples = pygame.sndarray.samples(base_sound)

        for index, sample in numpy.ndenumerate(samples):
            samples[index[0], index[1]] = math.sin(
                2.0 * math.pi * 440 * index[0] / 22050) * 28000

        del (samples)
        base_sound.play()


# Main code run!
App()