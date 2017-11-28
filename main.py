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
    sound_needs_updating = True  # Whether parameters have changed and the sound needs to be regenerated

    # Effects
    volume = 0  # Volume offset
    frequency = 1  # Frequency multiplier
    frequency_change = 0  # in multiplier per second (TODO)
    echo_count = 0  # Number of echoes

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
        if not self.sound_needs_updating:
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
        self.sound_needs_updating = False

    def init_ui(self):
        """Initialise ui elements."""

        top_frame = Tkinter.Frame(self.main_screen)
        play_preview = Tkinter.Button(top_frame, text="Play Sound", command=lambda: self.play_sound())
        play_preview.pack(side=Tkinter.LEFT)
        save_sound = Tkinter.Button(top_frame, text="Save Sound", command=lambda: self.save_sound())
        save_sound.pack(side=Tkinter.LEFT)

        volume_up = Tkinter.Button(self.main_screen, text="Volume Up", command=lambda: self.change_volume(10))
        volume_down = Tkinter.Button(self.main_screen, text="Volume Down", command=lambda: self.change_volume(-10))

        top_frame.pack()
        volume_up.pack()
        volume_down.pack()

    def run(self):
        """Runs the application."""

        # Initialise PyGame
        pygame.init()
        pygame.mixer.init(frequency=self.FREQUENCY, size=self.SIZE, channels=self.CHANNELS, buffer=self.BUFFER)

        # self.screen = pygame.display.set_mode((640, 481))  # 481 for extra uniqueness points

        # Initialise a base sine wave
        self.base_sound = self.create_sine(440, 1.0)

        self.main_screen = Tkinter.Tk()
        self.init_ui()
        self.main_screen.mainloop()

        # Generate a test sound with effects
        # self.edit_sound.play()
        self.edit_sound.change_frequency(0.5)
        self.edit_sound.change_volume(-0)

        wilhelm = DynSound("wilhelmscream.wav")
        self.edit_sound.mix(wilhelm)
        self.edit_sound.change_volume(-10)
        self.edit_sound.add_echo(0.3, -4, 10)

        self.edit_sound.save("testSound.wav")

    def quit(self):
        """Quits the application"""

        self.running = False

    def change_volume(self, offset):
        """Decreases the volume by offset

        Args:
            offset (float): The offset to increase (or decrease) volume by
        """
        self.volume += offset
        self.sound_needs_updating = True

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
