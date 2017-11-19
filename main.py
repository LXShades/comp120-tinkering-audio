import pygame
import numpy
import math
import wave
import struct


class App:

    """
    Sound editor app.

    Attributes:
        FREQUENCY (int): Frequency of sound.
        SIZE (int): Size of sound in bits.
        CHANNELS (int): Number of channels.
        BUFFER (int): Size of buffer.

        screen (pygame.Display): The main application screen.
        running (bool): If the program is running or not.
    """

    FREQUENCY = 22050
    SIZE = -16
    CHANNELS = 2
    BUFFER = 4096

    screen = None
    running = False

    # Temporary sound attribute
    sound = None

    def __init__(self):
        """Class constructor"""

        self.run()

    def run(self):
        """Run the application."""

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
        """Quits the application"""

        self.running = False

    def create_sine(self):
        """Creates an empty sound wave from the wilhelmScream (The origin of all life)"""

        self.sound = pygame.mixer.Sound("wilhelmScream.wav")
        samples = pygame.sndarray.samples(self.sound)

        for index, sample in numpy.ndenumerate(samples):
            samples[index[0], index[1]] = math.sin(
                2.0 * math.pi * 440 * index[0] / 22050) * 28000

        del samples

        self.change_frequency(self.sound, 0.5)
        self.change_volume(self.sound, -10)

        self.save_sound("testSound.wav", self.sound)

        self.sound.play()

    def save_sound(self, file_name, sound):
        """
        Saves a sound to disk.

        Args:
             file_name (string): The file name to save the sound with. File extension must be included.
             sound (pygame.mixer.Sound): The Sound to be saved.
        """
        samples = pygame.sndarray.samples(sound)

        saved_sound = wave.open(file_name, "w")
        saved_sound.setparams((samples.shape[1], math.fabs(self.SIZE / 8), self.FREQUENCY, samples.shape[0], "NONE", ""))

        sample_values = []

        for index, sample in numpy.ndenumerate(samples):
            packaged_value = struct.pack("<h", samples[index[0], index[1]])
            sample_values.append(packaged_value)

        value_string = "".join(sample_values)
        saved_sound.writeframes(value_string)

        saved_sound.close()

        samples = pygame.sndarray.samples(sound)

    def change_frequency(self, sound, multiplier):
        """
        Change the pitch of a sound.

        Args:
            sound (pygame.mixer.Sound): The sound to be altered.
            multiplier (float): The multiplier to be applied to the sound's frequency.
        """

        # Create a copy of the samples so we can resize them
        sample_array = pygame.sndarray.array(sound)

        if multiplier > 1.0:
            # Increase frequency
            for index, sample in numpy.ndenumerate(sample_array):
                if int(index[0] * multiplier) >= sample_array.shape[0]:
                    break
                else:
                    sample_array[index[0], index[1]] = sample_array[
                        int(index[0] * multiplier), index[1]]

            sample_array.resize((
                int(math.ceil(sample_array.shape[0] / float(multiplier))),
                int(sample_array.shape[1])))
        elif multiplier < 1.0:
            # Decrease frequency
            sample_array.resize((
                int(math.ceil(sample_array.shape[0] / float(multiplier))),
                int(sample_array.shape[1])))

            for frame in xrange(sample_array.shape[0] - 1, 0, -1):
                for channel in xrange(sample_array.shape[1]):
                    sample_array[frame, channel] = \
                        sample_array[int(frame * multiplier), channel]

        # Update the length of sound by copying data
        # (super efficient as always)
        self.sound = pygame.mixer.Sound(sample_array)

        del sample_array

    def change_volume(self, sound, db):
        """
        Change the volume of a sound.

        sound (pygame.mixer.Sound): The sound to alter.
        db (float): Decibels to change sound volume by.
        """

        sample_array = pygame.sndarray.samples(sound)

        multiplier = pow(10, float(db) / 20)
        for index, sample in numpy.ndenumerate(sample_array):
            # Todo limits checking (clipping)
            sample_array[index[0], index[1]] *= multiplier

        del sample_array


# Main code run!
App()