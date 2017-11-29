import Tkinter
import numpy

from generator import Generator


class UI:

    main_screen = None

    def __init__(self):
        """
        Constructor.

        Args:
            app (App): The class to get button functions from.
        """

        self.main_screen = Tkinter.Tk()

        self.init_ui()

    def init_ui(self):
        """Initialise ui elements."""

        # Play/Save buttons
        top_frame = Tkinter.Frame(self.main_screen)

        self.play_preview = Tkinter.Button(top_frame, text="Play Sound")
        self.play_preview.pack(side=Tkinter.LEFT)
        self.save_sound = Tkinter.Button(top_frame, text="Save Sound")
        self.save_sound.pack(side=Tkinter.LEFT)

        # Volume slider
        self.volume_slider = Tkinter.Scale(self.main_screen, troughcolor="#ff0000", orient=Tkinter.HORIZONTAL, from_=0, to=100, showvalue=False) # TODO: Fix clipping when increasing volume for greater range
        self.volume_slider.set(50)
        self.volume_slider.pack()

        # Frequency slider
        self.frequency_slider = Tkinter.Scale(self.main_screen, troughcolor="#ff0000", orient=Tkinter.HORIZONTAL, from_=0.1, to=5.0, resolution=0.1, showvalue=False)
        self.frequency_slider.set(1)
        self.frequency_slider.pack()

        # Echo slider
        self.echo_slider = Tkinter.Scale(self.main_screen, troughcolor="#0000ff", orient=Tkinter.HORIZONTAL, from_=0, to=10, showvalue=False)
        self.echo_slider.set(0)
        self.echo_slider.pack()

        top_frame.pack()

    def change_slider_colour(self, slider, (red, green, blue)):
        """Changes the colour of a slider by a red, green and blue value

        Args:
            slider (Tkinter.Scale): Tkinter slider object whose colour will be changed
            (red, green, blue) (int): Colour components between 0 and 255 (0x00-0xFF)
        """

        # Convert and clip colour values
        red = numpy.clip(int(red), 0, 0xFF)
        green = numpy.clip(int(green), 0, 0xFF)
        blue = numpy.clip(int(blue), 0, 0xFF)

        # Update slider
        slider.config(troughcolor="#" + format(int(blue | (green << 8) | (red << 16)), "06x"))
