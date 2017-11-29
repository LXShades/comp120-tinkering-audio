import math

import pygame
import numpy
import Tkinter
import tkMessageBox
import tkFileDialog

from dynsound import DynSound
from ui import UI
from generator import Generator


class App:
    """
    Sound editor app.

    Attributes:
        FREQUENCY (int): Frequency of sound.
        SIZE (int): Size of sound in bits.
        CHANNELS (int): Number of channels.
        BUFFER (int): Size of buffer.

        generator (Generator): App sound generator
        ui (UI): App user interface
    """

    FREQUENCY = 22050
    SIZE = -16
    CHANNELS = 2
    BUFFER = 4096

    generator = None
    ui = None

    def __init__(self):
        """Class constructor"""

        # Just call run and be done!
        self.run()

    def run(self):
        """Runs the application."""

        # Initialise PyGame
        pygame.init()
        pygame.mixer.init(frequency=self.FREQUENCY, size=self.SIZE, channels=self.CHANNELS, buffer=self.BUFFER)

        # Initialise ui and generator
        self.generator = Generator(self.FREQUENCY, self.SIZE, self.CHANNELS, self.BUFFER)
        self.ui = UI()

        # Initialise slider commands
        self.ui.play_preview.config(command=lambda: self.generator.play_sound())
        self.ui.save_sound.config(command=lambda: self.generator.save_sound())

        # Length slider
        self.ui.length_slider.config(command=lambda  value: self.on_slider_change(self.ui.length_slider, value))

        # Volume slider
        self.ui.volume_slider.config(command=lambda value: self.on_slider_change(self.ui.volume_slider, value)) # TODO: Fix clipping when increasing volume for greater range

        # Frequency slider
        self.ui.frequency_slider.config(command=lambda value: self.on_slider_change(self.ui.frequency_slider, value))

        # Frequency change slider
        self.ui.frequency_shift_slider.config(command=lambda value: self.on_slider_change(self.ui.frequency_shift_slider, value))

        # Echo slider
        self.ui.echo_slider.config(command=lambda value: self.on_slider_change(self.ui.echo_slider, value))

        # Plop slider
        self.ui.plop_slider.config(command=lambda value: self.on_slider_change(self.ui.plop_slider, value))

        # Begin main UI loop
        self.ui.main_screen.mainloop()

    def on_slider_change(self, slider, value):
        """
        Callback function called by the UI when one of the sliders changes

        Args:
            slider (Tkinter.Scale): A reference to the slider that's changed
            value (string): The value of the slider as provided by Tkinter
        """
        # Update sliders and change their colours on a per-slider basis

        if slider == self.ui.length_slider:
            self.generator.sound_length = float(value)
            self.generator.sound_valid = False

            # Make slidar DED ARD!!!
            black_factor = int(value) * 255 / 10

            self.ui.change_slider_colour(self.ui.length_slider, (255 - black_factor, 255 - black_factor, 255 - black_factor))
        elif slider == self.ui.volume_slider:
            new_volume = float(value)
            self.generator.change_volume(new_volume - 100)

            # Giv slidar BIG BOOM YELLOZ
            self.ui.change_slider_colour(self.ui.volume_slider, (int(new_volume + 100) * 255 / 100, int(new_volume + 100) * 255 / 100, 0))
        elif slider == self.ui.echo_slider:
            self.generator.change_echoes(int(value))

            # Make slider da sneakistz purppl
            self.ui.change_slider_colour(self.ui.echo_slider, (0x80 + int(value) * 0x7F / 10, 0, 0x80 + int(value) * 0x7F / 10))
        elif slider == self.ui.frequency_slider:
            self.generator.change_frequency(float(value))

            # Make slider SUPA FAST!!
            frequency_factor = int(float(value) * 255 / 5)
            self.ui.change_slider_colour(self.ui.frequency_slider, (frequency_factor, 0, 128 - frequency_factor / 2))
        elif slider == self.ui.frequency_shift_slider:
            self.generator.change_frequency_shift(float(value))

            # Make slidar LUCKY
            self.ui.change_slider_colour(self.ui.frequency_shift_slider, (50, 50, float(value) * 255 / 5))
        elif slider == self.ui.plop_slider:
            self.generator.change_plopper(float(value))

            # Sound like DEFF! AAAAGH!
            self.ui.change_slider_colour(self.ui.plop_slider, (0, 255 - (int(value) * 255 / 100), 0))

# Main code run!
App()
