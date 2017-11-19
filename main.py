import math

import pygame
import numpy

from dynsound import DynSound


class App:
    FREQUENCY = 22050
    SIZE = -16
    CHANNELS = 2
    BUFFER = 4096

    screen = None
    running = False

    def __init__(self):
        self.run()

    def run(self):
        pygame.init()
        pygame.mixer.init(frequency=self.FREQUENCY, size=self.SIZE, channels=self.CHANNELS, buffer=self.BUFFER)

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
        self.running = False

    def create_sine(self):
        sound = DynSound(num_frames=22050)
        #sound = DynSound(num_frames=22050)
        samples = pygame.sndarray.samples(sound.sound)

        packaged_value = None

        for index, sample in numpy.ndenumerate(samples):
            samples[index[0], index[1]] = math.sin(
                2.0 * math.pi * 440 * index[0] / 22050) * 28000

        del samples

        sound.change_frequency(0.5)
        sound.change_volume(-10)

        sound.save("testSound.wav")

        sound.play()


# Main code run!
App()