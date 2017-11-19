import struct
import wave
import math

import numpy
import pygame


class DynSound:
    """DynSound: A dynamic sound (editable sound) based on pygame.Sound

        Attributes:
            sound (pygame.Sound): source sound
    """
    sound = None
    num_channels = 0
    sample_rate = 0

    def __init__(self, file_name):
        """___init___: Create sound from file"""
        self.sound = pygame.mixer.Sound(file_name)
        self.num_channels = 2

        self.sample_rate = 22050

    def __init__(self, load_file="", num_channels=2, num_frames=1, sample_rate=22050, data_type="<i2"):
        """Create empty sound or loads a file if load_file is not ""
            Args:
                load_file: Filename to load (overrides other arguments!)
                num_channels: Number of channel in the sound
                num_frames: Length of the sound in frames
                sample_rate: Sample rate of sound
                data_type: Type of data for samples. Usually signed 2-byte int
        """
        if load_file:
            self.sound = pygame.mixer.Sound(load_file)
            self.num_channels = 2  # TO FIX
            self.sample_rate = 22050  # ALSO TO FIX LOL

            if self.sound.get_length() <= 0.1:
                # Assume load failed
                del self.sound
                self.sound = None

        # If no sound was provided or loaded, create an empty sound
        if self.sound is None:
            self.sound = pygame.mixer.Sound(
                numpy.ndarray(shape=(num_frames, num_channels), dtype=data_type))
            self.num_channels = num_channels
            self.sample_rate = sample_rate

    def save(self, file_name):
        """
        Saves a sound to disk.

        Args:
             file_name (string): The file name to save the sound with. File extension must be included.
        """
        samples = pygame.sndarray.samples(self.sound)

        saved_sound = wave.open(file_name, "w")
        saved_sound.setparams((samples.shape[1], self.num_channels,
                               self.sample_rate, samples.shape[0], "NONE", ""))

        sample_values = []

        for index, sample in numpy.ndenumerate(samples):
            packaged_value = struct.pack("<h", samples[index[0], index[1]])
            sample_values.append(packaged_value)

        value_string = "".join(sample_values)
        saved_sound.writeframes(value_string)

        saved_sound.close()

    def change_frequency(self,  multiplier):
        """
        Change the pitch of a sound.

        Args:
            sound (pygame.mixer.Sound): The sound to be altered.
            multiplier (float): The multiplier to be applied to the sound's frequency.
        """
        # Create a copy of the samples so we can resize them
        sample_array = pygame.sndarray.array(self.sound)

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

    def change_volume(self, db):
        """
        Change the volume of a sound.

        sound (pygame.mixer.Sound): The sound to alter.
        db (float): Decibels to change sound volume by.
        """
        sample_array = pygame.sndarray.samples(self.sound)

        multiplier = pow(10, float(db) / 20)
        for index, sample in numpy.ndenumerate(sample_array):
            # Todo limits checking (clipping)
            sample_array[index[0], index[1]] *= multiplier

    def play(self):
        """Play the sound"""
        self.sound.play()