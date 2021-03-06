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
    sample_range = 0
    sample_min = 0
    sample_max = 0

    def __init__(self, file_name):
        """___init___: Create sound from file"""

        self.sound = pygame.mixer.Sound(file_name)
        self.num_channels = 2

        self.sample_rate = 22050

    def __init__(self, load_file="", num_frames=1, num_channels=2, sample_rate=22050, data_type="<h"):
        """Create empty sound or loads a file if load_file is not "".

        Args:
            load_file: Filename to load. Overrides num_frames
            num_frames: Length of the sound in frames. Used if load_file is N/A, to decide the length of the default wave
            num_channels: Number of channels in the mixer. This must match pygame.mixer's initialisation values.
            sample_rate: Sample rate. This must match pygame.mixer's initialised values.
            data_type: Type of data for samples. Usually signed 2-byte int. This must match pygame.mixer's initialised data type.
        """

        # Load a file if a filename was provided
        if load_file:
            self.sound = pygame.mixer.Sound(load_file)

            if self.sound.get_length() <= 0.1:
                # Assume that the load failed
                del self.sound
                self.sound = None

        # If no sound was provided or loaded, create an empty sound
        if self.sound is None:
            self.sound = pygame.mixer.Sound(numpy.ndarray(shape=(num_frames, num_channels), dtype=data_type))

        # Set sound parameters
        self.num_channels = num_channels
        self.sample_rate = sample_rate

        if data_type.islower():
            self.sample_range = (1 << (struct.calcsize(data_type) * 8)) - 1
            self.sample_min = -self.sample_range / 2 # signed range
            self.sample_max = self.sample_range / 2
        else:
            self.sample_range = (1 << (struct.calcsize(data_type) * 8)) - 1  # unsigned range
            self.sample_min = 0
            self.sample_max = self.sample_range

    def copy(self):
        """Creates and returns a copy of this sound

        Returns:
            (Sound) The copy
        """

        samples = pygame.sndarray.samples(self.sound)

        new_sound = DynSound(num_channels=self.num_channels, num_frames=samples.shape[0], sample_rate=self.sample_rate)
        new_sound.sound = pygame.mixer.Sound(samples)

        return new_sound

    def save(self, file_name):
        """
        Saves this sound to disk.

        Args:
             file_name (string): The file name to save the sound with. File extension must be included.
        """

        samples = pygame.sndarray.samples(self.sound)

        # Create/open WAV
        saved_sound = wave.open(file_name, "w")
        saved_sound.setparams((samples.shape[1], self.num_channels, self.sample_rate, samples.shape[0], "NONE", ""))

        # Write samples to WAV
        sample_values = []

        for index, sample in numpy.ndenumerate(samples):
            packaged_value = struct.pack("<h", samples[index[0], index[1]])
            sample_values.append(packaged_value)

        value_string = "".join(sample_values)
        saved_sound.writeframes(value_string)

        # Done!
        saved_sound.close()

    def resize(self, num_frames):
        """Resizes this sound to a precise number of frames

        Args:
            num_frames (int): New length of the sound, in frames
        """

        # Create a copy of the sound's samples (surprise! This seems to be the only way we can resize it).
        sample_array = pygame.sndarray.array(self.sound)

        sample_array.resize((num_frames, sample_array.shape[1]))

        self.sound = pygame.mixer.Sound(sample_array)

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

        # Determine the frame max and min boundaries for both sounds
        target_start_frame = int(target_start * self.sample_rate)
        source_start_frame = int(source_start * self.sample_rate)
        num_frames = int(length * self.sample_rate)
        num_channels = self.num_channels

        if source_start_frame + num_frames >= source_samples.shape[0] or length == -1:
            num_frames = source_samples.shape[0] - source_start_frame

        # Load the target (self) samples
        sample_array = pygame.sndarray.array(self.sound)

        if sample_array.shape[0] < target_start_frame + num_frames:
            sample_array.resize((target_start_frame + num_frames, sample_array.shape[1]))

        # Mix the sounds!
        for frame in xrange(0, num_frames):
            for channel in xrange(0, num_channels):
                sample_array[target_start_frame + frame, channel] = numpy.clip(int(sample_array[target_start_frame + frame, channel]) + source_samples[source_start_frame + frame, channel],
                                                                               self.sample_min, self.sample_max)

        # Copy the data back into this sound
        self.sound = pygame.mixer.Sound(sample_array)

    def add_echo(self, delay, volume_change, num_echoes):
        """
        Adds an echo to the sound.

        Args:
            delay (float): Delay of each echo, in seconds
            volume_change (float): Reduction of volume per echo, in dB
            num_echoes (int): Number of echoes
        """

        original_sound = self.copy()

        for i in xrange(0, num_echoes):
            overlay = original_sound.copy()
            overlay.change_volume(volume_change * (i + 1))
            self.mix(overlay, delay * (i + 1))

    def change_frequency(self,  multiplier):
        """
        Change the pitch of a sound.

        Args:
            multiplier (float): The multiplier to be applied to the sound's frequency.
        """

        # Create a copy of the samples so we can resize them
        sample_array = pygame.sndarray.array(self.sound)

        if multiplier > 1.0:
            # Increase frequency (shift down samples from later on in the array)
            for index, sample in numpy.ndenumerate(sample_array):
                if int(index[0] * multiplier) >= sample_array.shape[0]:
                    break
                else:
                    sample_array[index[0], index[1]] = sample_array[int(index[0] * multiplier), index[1]]

            sample_array.resize((int(math.ceil(sample_array.shape[0] / float(multiplier))), int(sample_array.shape[1])))
        elif multiplier < 1.0:
            # Decrease frequency (stretch out samples from earlier on in the array)
            sample_array.resize((int(math.ceil(sample_array.shape[0] / float(multiplier))), int(sample_array.shape[1])))

            for frame in xrange(sample_array.shape[0] - 1, 0, -1):
                for channel in xrange(sample_array.shape[1]):
                    sample_array[frame, channel] = sample_array[int(frame * multiplier), channel]

        # Update the length of sound by recreating it (seems to be the only way to resize a sound)
        self.sound = pygame.mixer.Sound(sample_array)

    def change_frequency_shifting(self,  multiplier, multiplier_shift):
        """
        Change the pitch of the sound with a constant shift up or down during playback

        Args:
            multiplier (float): The base multiplier to be applied to the sound's frequency.
            multiplier_shift (float): The amount by which the multiplier increases per second
        """

        # Create a copy of the samples so we can resize them
        sample_array = pygame.sndarray.array(self.sound)

        for index, sample in numpy.ndenumerate(sample_array):
            grab = int(index[0] * (multiplier + float(index[0]) / self.sample_rate * multiplier_shift))

            if grab >= sample_array.shape[0] or grab < 0:
                break
            else:
                sample_array[index[0], index[1]] = sample_array[grab, index[1]]

        sample_array.resize((int(math.ceil(sample_array.shape[0] / float(multiplier + float(sample_array.shape[0]) / self.sample_rate * multiplier_shift))), int(sample_array.shape[1])))

        # Update the length of sound by recreating it (seems to be the only way to resize a sound)
        self.sound = pygame.mixer.Sound(sample_array)

    def change_volume(self, db):
        """
        Change the volume of a sound.

        Args:
            db (float): Decibels to change sound volume by.
        """

        sample_array = pygame.sndarray.samples(self.sound)

        # Multiply all samples according to the dB given
        multiplier = pow(10, float(db) / 20)
        for index, sample in numpy.ndenumerate(sample_array):
            # Todo limits checking (clipping)
            sample_array[index[0], index[1]] = numpy.clip(sample_array[index[0], index[1]] * multiplier, self.sample_min, self.sample_max)

    def add_plopper(self, plopper_rate):
        """
        Adds 'plop' effect. Plop effect is a stutter/on-off effect.

        Args:
             plopper_rate (float): Number of plops per second
        """

        # Don't divide by extremely small amounts (slight hack: checking if it is 0.0 has given me errors in the past where Python divided by zero anyway, so using 0.0001)
        if plopper_rate <= 0.0001:
            return

        # Produce plop effect
        sample_array = pygame.sndarray.samples(self.sound)

        high_index = self.sample_rate / plopper_rate / 2
        length = sample_array.shape[0]
        while high_index < length:
            section_end = high_index + self.sample_rate / plopper_rate / 2

            if section_end > length:
                section_end = length

            for low_index in xrange(int(high_index), int(section_end)):
                for channel in xrange(0, self.num_channels):
                    sample_array[low_index, channel] = 0

            high_index += self.sample_rate / plopper_rate

    def play(self):
        """Play the sound"""

        self.sound.play()
