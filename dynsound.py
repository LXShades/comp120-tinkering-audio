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

    def copy(self):
        """Creates and returns a copy of this sound

             Returns: (Sound) The copy
        """
        samples = pygame.sndarray.samples(self.sound)

        new_sound = DynSound(num_channels=self.num_channels, num_frames=samples.shape[0], sample_rate=self.sample_rate)
        new_sound.sound = pygame.mixer.Sound(samples)

        return new_sound

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

    def mix(self, source, target_start=0.0, source_start=0.0, length=-1):
        """Mixes this sound with another

        Args:
            source (DynSound): Sound to mix with
            target_start (float in seconds): Time, in this sound, to start mixing at
            source_start (float in seconds): Time, in sound2, to start the mix
            length (float in seconds): Length of the sound section being mixed.
                                       -1 will use the length of the source sound
        """
        # Load the source samples
        source_samples = pygame.sndarray.array(source.sound)

        # Determine frame boundaries for mix
        target_start_frame = int(target_start * self.sample_rate)
        source_start_frame = int(source_start * self.sample_rate)
        num_frames = int(length * self.sample_rate)
        num_channels = 2  # TODO

        if source_start_frame + num_frames >= source_samples.shape[0] or length == -1:
            num_frames = source_samples.shape[0] - source_start_frame

        # Load the target (self) samples
        sample_array = pygame.sndarray.array(self.sound)

        if sample_array.shape[0] < target_start_frame + num_frames:
            sample_array.resize((target_start_frame + num_frames, sample_array.shape[1]))

        # Mix the sounds!
        for frame in xrange(0, num_frames):
            # TODO: handle clipping
            # TODO: further consideration--mixing mono with stereo sounds
            for channel in xrange(0, num_channels):
                sample_array[target_start_frame + frame, channel] += source_samples[source_start_frame + frame, channel]

        # Copy the data back into this sound
        self.sound = pygame.mixer.Sound(sample_array)

    def add_echo(self, delay, volume_change, num_echoes):
        """Adds an echo to the sound
        Args:
            delay (float): Delay of each echo, in seconds
            volume_change (float): Reduction of volume per echo, in dB
            num_echoes (int): Number of echoes
        """
        original_sound = self.copy()
        for i in xrange(0, num_echoes):
            shut_up = original_sound.copy()
            shut_up.change_volume(volume_change * (i + 1))
            self.mix(shut_up, delay * (i + 1))

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

