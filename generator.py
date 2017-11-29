import math
import pygame
import Tkinter
import tkFileDialog
import numpy

from dynsound import DynSound


class Generator:
    """
    Variables and functions for app.

    Attributes:
        mixer_sample_rate (int): Sample rate of mixer.
        mixer_sample_size (int): Size of sound samples in bits (negative if signed, positive if unsigned, blame pygame).
        mixer_num_channels (int): Number of sound channels in mixer.
        mixer_buffer_size (int): Size of mixer buffer.

        edit_sound (DynSound): Sound after edits have been applied
        base_sound (DynSound): Original sound before edits are applied
        sound_valid (boolean): Whether the sound is valid. If invalid, sound will be validated before being played or saved

        volume (float): Volume offset effect
        frequency (float): Frequency multiplier for sound
        frequency_shift (float): Rate of frequency increase or decrease over time
        echo_count (int): Number of echoes to follow the sound
        plops_per_second (int): Plop effect for sounds
    """

    mixer_sample_rate = 22050
    mixer_sample_size = -16
    mixer_num_channels = 2
    mixer_buffer_size = 4096

    edit_sound = None
    base_sound = None
    sound_valid = False

    volume = 0  # Volume offset
    frequency = 1  # Frequency multiplier
    frequency_shift = 0  # in multiplier per second (TODO)
    echo_count = 0  # Number of echoes
    plops_per_second = 0

    # User interface
    volume_slider = None
    frequency_slider = None
    echo_slider = None

    def __init__(self, sample_rate, sample_size, num_channels, buffer_size):
        """
        Initialises sound generator with a base sine wave

        Args:
            sample_rate (int): Sample rate of mixer. Must match pygame.mixer initialisation properties.

        """

        self.mixer_sample_rate = sample_rate
        self.mixer_buffer_size = buffer_size
        self.mixer_num_channels = num_channels
        self.mixer_buffer_size = buffer_size
        self.base_sound = self.create_sine(440, 1.0)

    def play_sound(self):
        """Previews the sound"""

        self.validate_sound()
        self.edit_sound.play()

    def save_sound(self):
        """Saves the sound as a WAV with a user-selected name"""

        self.validate_sound()

        # Give the user a prompt to save the sound
        filename = tkFileDialog.asksaveasfilename(initialdir="/", title="Save WAV as...", filetypes=[("Wave files", "*.wav")])

        # Save it (unless the user cancelled)
        if filename is not "":
            self.edit_sound.save(filename)

    def validate_sound(self):
        """Regenerate sound from base elements"""

        if self.sound_valid:
            return

        # Regenerate the 2-second A4 base sine wave (note: in a stretch-goal version the user could select the base sound)
        self.base_sound = self.create_sine(440, self.frequency)  # self.frequency is used to rebalance the length of the final sound before change_frequency is called

        # Recopy the base sound
        self.edit_sound = self.base_sound.copy()

        # Apply effects in an order which hopefully minimises clipping: volume, frequency, plops, echoes
        if self.volume is not 0:
            self.edit_sound.change_volume(self.volume)

        if self.frequency != 1.0 and self.frequency_shift == 0.0:
            self.edit_sound.change_frequency(self.frequency)
        elif self.frequency_shift != 0.0:
            self.edit_sound.change_frequency_shifting(self.frequency, self.frequency_shift)

        if self.plops_per_second > 0:
            self.edit_sound.add_plopper(self.plops_per_second)

        if self.echo_count > 0:
            self.edit_sound.add_echo(0.3, -4, self.echo_count)

        # Validate sound
        self.sound_valid = True

    def change_volume(self, new_volume):
        """
        Sets the volume of the main edited sound

        Args:
            new_volume (float): The offset to increase (or decrease) volume by.
        """

        # Change colour of slider when volume is changed (white to black)
        self.volume = new_volume
        self.sound_valid = False

    def change_frequency(self, frequency_multiplier):
        """
        Sets the frequency of the main edited sound

        Args:
            frequency_multiplier (float): The new multiplier for the sound frequency
        """

        self.frequency = float(frequency_multiplier)
        self.sound_valid = False

    def change_frequency_shift(self, frequency_shift):
        """
        Sets the frequency shift of the main edited sound

        Args:
            frequency_shift (float): The new rate of shift for frequency, in multipliers / sec
        """

        self.frequency_shift = frequency_shift
        self.sound_valid = False

    def change_echoes(self, echo_num):
        """
        Set the number of echoes.

        Args:
            echo_num (int): Number of echoes to add.
        """

        self.echo_count = echo_num
        self.sound_valid = False

    def change_plopper(self, plops_per_second):
        """
        Sets plops per second

        Args:
            plops_per_second (float): Number of plops per second (sound effect)
        """

        self.plops_per_second = plops_per_second
        self.sound_valid = False

    def create_sine(self, frequency, length):
        """
        Creates a sine wave

        Args:
            frequency (int): Frequency of the sine wave in hZ
            length (float): Length of the sine wave in seconds
        Returns:
            (DynSound) A sine wave
        """

        sound = DynSound(num_frames=int(length * self.mixer_sample_rate))
        samples = pygame.sndarray.samples(sound.sound)

        minimum_value = sound.sample_min
        maximum_value = sound.sample_max
        centre_value = (minimum_value + maximum_value) / 2
        sample_range = sound.sample_max - centre_value

        for index, sample in numpy.ndenumerate(samples):
            samples[index[0], index[1]] = centre_value + math.sin(2.0 * math.pi * frequency * index[0] / self.mixer_sample_rate) * sample_range

        del samples

        return sound
