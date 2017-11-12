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

        self.change_frequency(samples, 2)
        self.change_volume(samples, -10)

        del (samples)
        base_sound.play()

    # sample access at 'time' for left: sample[time, 0]
    # sample access at 'time' for right: sample[time, 1]
    # first sample (left): sample[0, 0]
    # first sample (right): sample[0, 1]
    # second sample (left): sample[1, 0]
    # second sample (right): sample[1, 1]
    def change_frequency(self, sample_array, multiplier):
        for index, sample in numpy.ndenumerate(sample_array):
            if (index[0] * multiplier) >= (sample_array.shape[0]):
                break
            else:
                sample_array[index[0], index[1]] = sample_array[
                    index[0] * multiplier, index[1]]

    def change_volume(self, sample_array, db):
        multiplier = pow(10, float(db) / 20)
        for index, sample in numpy.ndenumerate(sample_array):
            # Todo limits checking (clipping)
            sample_array[index[0], index[1]] *= multiplier


# Main code run!
App()