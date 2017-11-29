import math

import pygame
import numpy
import Tkinter
import tkMessageBox
import tkFileDialog

from dynsound import DynSound


class App:
    """
    Sound editor app.

    Attributes:
        FREQUENCY (int): Frequency of sound.
        SIZE (int): Size of sound in bits.
        CHANNELS (int): Number of channels.
        BUFFER (int): Size of buffer.

        main_screen (Tkinter.Tk): The main application screen.
        running (bool): If the program is running or not.
    """

    FREQUENCY = 22050
    SIZE = -16
    CHANNELS = 2
    BUFFER = 4096

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

    def __init__(self):
        """Class constructor"""

        # Just call run and be done!
        self.run()

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

    def init_ui(self):
        """Initialise ui elements."""

        # Play/Save buttons
        top_frame = Tkinter.Frame(self.main_screen)

        play_preview = Tkinter.Button(top_frame, text="Play Sound", command=lambda: self.play_sound())
        play_preview.pack(side=Tkinter.LEFT)
        save_sound = Tkinter.Button(top_frame, text="Save Sound", command=lambda: self.save_sound())
        save_sound.pack(side=Tkinter.LEFT)

        # Volume slider
        self.volume_slider = Tkinter.Scale(self.main_screen, troughcolor="#ff0000", orient=Tkinter.HORIZONTAL, from_=0, to=100, command=lambda v: self.change_volume(float(v) - 100)) # TODO: Fix clipping when increasing volume for greater range
        self.volume_slider.set(50)
        self.volume_slider.pack()

        # Frequency slider
        self.frequency_slider = Tkinter.Scale(self.main_screen, troughcolor="#ff0000", orient=Tkinter.HORIZONTAL, from_=0.1, to=5.0, resolution=0.1, command=lambda v: self.change_frequency(float(v)))
        self.frequency_slider.set(1)
        self.frequency_slider.pack()

        top_frame.pack()

    def run(self):
        """Runs the application."""

        # Initialise PyGame
        pygame.init()
        pygame.mixer.init(frequency=self.FREQUENCY, size=self.SIZE, channels=self.CHANNELS, buffer=self.BUFFER)


        # Initialise a base sine wave
        self.base_sound = self.create_sine(440, 1.0)

        self.main_screen = Tkinter.Tk()
        self.init_ui()
        self.main_screen.mainloop()

        # Generate a test sound with effects
        # self.edit_sound.play()
        # self.edit_sound.change_frequency(0.5)
        # self.edit_sound.change_volume(-0)

        wilhelm = DynSound("wilhelmscream.wav")
        self.edit_sound.mix(wilhelm)
        self.edit_sound.change_volume(-10)
        self.edit_sound.add_echo(0.3, -4, 10)

        self.edit_sound.save("testSound.wav")

    def quit(self):
        """Quits the application"""

        self.running = False

    def change_volume(self, new_volume):
        """Sets the volume of the main edited sound

        Args:
            new_volume (float): The offset to increase (or decrease) volume by.
        """

        # Change colour of slider when volume is changed (white to black)
        normalised_volume = int((new_volume + 100) * 255 / 100)
        new_colour = "#" + format(0xFFFFFF - normalised_volume - (normalised_volume << 8) - (normalised_volume << 16), "06x")

        self.volume = new_volume
        self.volume_slider.config(troughcolor=new_colour)
        self.sound_valid = False

    def change_frequency(self, frequency_multiplier):
        """Sets the frequency of the main edited sound

        Args:
            frequency_multiplier (float): The new multiplier for the sound frequency
        """
        new_colour = "#" + format(int(frequency_multiplier * 255 / 5), "02x") + "0000"

        self.frequency = frequency_multiplier
        self.frequency_slider.config(troughcolor=new_colour)
        self.sound_valid = False

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
            samples[index[0], index[1]] = math.sin(2.0 * math.pi * frequency * index[0] / 22050) * 32767

        del samples

        return sound


# Main code run!
App()
