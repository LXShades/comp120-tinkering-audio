import math

import pygame
import numpy
import Tkinter
import tkMessageBox

from dynsound import DynSound


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

    main_screen = None
    running = False
    edit_sound = None

    def __init__(self):
        """Class constructor"""

        # Just call run and be done!
        self.run()

    def helloCallBack(self):
        tkMessageBox.showinfo("Hello Python", "Hello World")



    def init_ui(self):
        """Initialise ui elements."""

        play_preview = Tkinter.Button(self.main_screen, text="Play Sound", command=lambda: pygame.mixer.Sound.play(self.edit_sound.sound))

        volume_up = Tkinter.Button(self.main_screen, text="Volume Up", command=self.edit_sound.change_volume(10))
        volume_down = Tkinter.Button(self.main_screen, text="Volume Down", command=self.edit_sound.change_volume(-10))

        play_preview.pack()
        volume_up.pack()
        volume_down.pack()

    def run(self):
        """Runs the application."""

        # Initialise PyGame
        pygame.init()
        pygame.mixer.init(frequency=self.FREQUENCY, size=self.SIZE, channels=self.CHANNELS, buffer=self.BUFFER)

        # self.screen = pygame.display.set_mode((640, 481))  # 481 for extra uniqueness points

        self.edit_sound = self.create_sine(440, 1.0)

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