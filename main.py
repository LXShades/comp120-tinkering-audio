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
        SAMPLE_RANGE (int): Approximate min and max range of sound samples

        main_screen (Tkinter.Tk): The main application screen.
        running (bool): If the program is running or not.
    """

    FREQUENCY = 22050
    SIZE = -16
    CHANNELS = 2
    BUFFER = 4096
    SAMPLE_RANGE = 32767

    running = False

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

        # Initialise a base sine wave
        #self.base_sound = self.create_sine(440, 1.0)

        # Initialise ui and generator
        self.generator = Generator()
        self.ui = UI()

        # Initialise slider commands
        self.ui.play_preview.config(command=lambda: self.generator.play_sound())
        self.ui.save_sound.config(command=lambda: self.generator.save_sound())

        # Volume slider
        self.ui.volume_slider.config(command=lambda v: self.generator.change_volume(float(v) - 100)) # TODO: Fix clipping when increasing volume for greater range

        # Frequency slider
        self.ui.frequency_slider.config(command=lambda v: self.generator.change_frequency(self.ui, float(v)))

        # Echo slider
        self.ui.echo_slider.config(command=lambda v: self.generator.change_echoes(int(v)))

        self.ui.main_screen.mainloop()

        # TODO testing new ui
        #self.main_screen = Tkinter.Tk()
        #self.init_ui()
        #self.main_screen.mainloop()

        # Generate a test sound with effects
        # self.edit_sound.play()
        # self.edit_sound.change_frequency(0.5)
        # self.edit_sound.change_volume(-0)

        wilhelm = DynSound("wilhelmscream.wav")
        # self.edit_sound.mix(wilhelm)
        # self.edit_sound.change_volume(-10)
        # self.edit_sound.add_echo(0.3, -4, 10)

        # self.edit_sound.save("testSound.wav")

    def quit(self):
        """Quits the application"""

        self.running = False

# Main code run!
App()
