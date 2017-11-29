import math
import pygame
import Tkinter
import tkFileDialog
import numpy

from dynsound import DynSound


# TODO: find a better name than data
class Generator:
    """
    Variables and functions for app.

    Attributes:
        FREQUENCY (int): Frequency of sound.
        SIZE (int): Size of sound in bits.
        CHANNELS (int): Number of channels.
        BUFFER (int): Size of buffer.
        SAMPLE_RANGE (int): Approximate min and max range of sound samples

        main_screen (Tkinter.Tk): The main application screen.
        running (bool): If the program is running or not.
    """

    FREQUENCY = 22050
    SIZE = -16
    CHANNELS = 2
    BUFFER = 4096
    SAMPLE_RANGE = 32767

    main_screen = None
    running = False
    edit_sound = None
    base_sound = None  # Original loaded sound or sine wave
    sound_valid = False  # Whether parameters have changed and the sound needs to be regenerated

    # Effects
    volume = 0  # Volume offset
    frequency = 1  # Frequency multiplier
    frequency_change = 0  # in multiplier per second (TODO)
    echo_count = 0  # Number of echoes

    # User interface
    volume_slider = None
    frequency_slider = None
    echo_slider = None

    def __init__(self):
        self.base_sound = self.create_sine(440, 1.0)

    def play_sound(self):
        self.validate_sound()
        self.edit_sound.play()

    def save_sound(self):
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

        # Recopy the base sound
        self.edit_sound = self.base_sound.copy()

        # Apply effects in an order which hopefully minimises clipping: volume, frequency, echoes
        if self.volume is not 0:
            self.edit_sound.change_volume(self.volume)

        if self.frequency is not 1.0:
            self.edit_sound.change_frequency(self.frequency)

        if self.echo_count > 0:
            self.edit_sound.add_echo(0.3, -4, self.echo_count)

        # Validate sound
        self.sound_valid = True

    def change_volume(self, new_volume):
        """Sets the volume of the main edited sound

        Args:
            new_volume (float): The offset to increase (or decrease) volume by.
        """

        # Change colour of slider when volume is changed (white to black)
        self.volume = new_volume
        self.sound_valid = False

        # self.change_slider_colour(self.ui.volume_slider, (int(new_volume + 100) * 255 / 100, int(new_volume + 100) * 255 / 100, 0))

    def change_frequency(self, ui, frequency_multiplier):
        """Sets the frequency of the main edited sound

        Args:
            frequency_multiplier (float): The new multiplier for the sound frequency
        """
        self.frequency = frequency_multiplier
        self.sound_valid = False

        # Make slider SUPA FAST!!
        ui.change_slider_colour(ui.frequency_slider, (int(frequency_multiplier * 255 / 5), 0, 0))

    def change_echoes(self, echo_num):
        """Set the number of echoes.

        Args:
            echo_num (int): Number of echoes to add.
        """

        self.echo_count = echo_num
        self.sound_valid = False

        # Make slider da sneakistz purppl
        # self.change_slider_colour(self.ui.echo_slider, (0x80 + int(echo_num) * 0x7F / 10, 0, 0x80 + int(echo_num) * 0x7F / 10))

    def create_sine(self, frequency, length):
        """Creates a sine wave

        Args:
            frequency (int): Frequency of the sine wave in hZ
            length (float): Length of the sine wave in seconds
        Returns:
            (DynSound) A sine wave
        """
        sound = DynSound(num_frames=int(length * 22050))
        samples = pygame.sndarray.samples(sound.sound)

        for index, sample in numpy.ndenumerate(samples):
            samples[index[0], index[1]] = math.sin(2.0 * math.pi * frequency * index[0] / 22050) * self.SAMPLE_RANGE

        del samples

        return sound