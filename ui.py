import Tkinter
import numpy

from generator import Generator


class UI:
    """
    UI class. Contains the UI elements and presets.

    Attributes:
        main_screen (Tkinter.Tk): The main application screen.

        play_preview (Tkinter.Button): Button to preview the sound.
        save_sound (Tkinter.Button): Button to sound the sound.
        volume_slider (Tkinter.Scale): Slider for the volume.
        frequency_slider (Tkinter.Scale): Slider for the frequency.
        frequency_shift_slider (Tkinter.Scale): Slider for the step up in frequency per second.
        echo_slider (Tkinter.Scale): Slider for the echoes.
        plop slider (Tkinter.Scale): Slider for the 'plops' or on-off stutters.

        death_preset_button (Tkinter.Button): Button to set sliders to death sound preset.
        jump_preset_button (Tkinter.Button): Button to set sliders to jump sound preset.
        pickup_preset_button (Tkinter.Button): Button to set sliders to pickup sound preset.
        laser_preset_button (Tkinter.Button): Button to set sliders to laser sound preset.
    """

    main_screen = None

    play_preview = None
    save_sound = None

    volume_slider = None
    frequency_slider = None
    frequency_shift_slider = None
    echo_slider = None
    plop_slider = None  # TODO: Not per second for some reason?

    death_preset_button = None
    jump_preset_button = None
    pickup_preset_button = None
    laser_preset_button = None

    def __init__(self):
        """Initialises and sets up the user interface"""

        self.main_screen = Tkinter.Tk()

        self.init_ui()

    def init_ui(self):
        """Initialise ui elements."""

        top_frame = Tkinter.Frame(self.main_screen)

        # Preset sound buttons.
        self.death_preset_button = Tkinter.Button(top_frame, text="Death Sound", command=lambda: self.death_preset())
        self.death_preset_button.pack(side=Tkinter.RIGHT)

        self.jump_preset_button = Tkinter.Button(top_frame, text="Jump Sound", command=lambda: self.jump_preset())
        self.jump_preset_button.pack(side=Tkinter.RIGHT)

        self.pickup_preset_button = Tkinter.Button(top_frame, text="Pickup Sound", command=lambda: self.pickup_preset())
        self.pickup_preset_button.pack(side=Tkinter.RIGHT)

        self.laser_preset_button = Tkinter.Button(top_frame, text="Laser Sound", command=lambda: self.pickup_preset())
        self.laser_preset_button.pack(side=Tkinter.RIGHT)

        # Play/Save buttons
        self.play_preview = Tkinter.Button(top_frame, text="Play Sound")
        self.play_preview.pack(side=Tkinter.LEFT)
        self.save_sound = Tkinter.Button(top_frame, text="Save Sound")
        self.save_sound.pack(side=Tkinter.LEFT)

        # Volume slider
        self.volume_slider = Tkinter.Scale(self.main_screen, troughcolor="#FFFF00", orient=Tkinter.HORIZONTAL, from_=0, to=100, showvalue=True)
        self.volume_slider.set(100)
        self.volume_slider.pack()

        # Frequency slider
        self.frequency_slider = Tkinter.Scale(self.main_screen, troughcolor="#000000", orient=Tkinter.HORIZONTAL, from_=0.1, to=5.0, resolution=0.1, showvalue=True)
        self.frequency_slider.set(1)
        self.frequency_slider.pack()

        # Frequency shift slider
        self.frequency_shift_slider = Tkinter.Scale(self.main_screen, troughcolor="#ff0000", orient=Tkinter.HORIZONTAL, from_=0, to=5.0, resolution=0.1, showvalue=True)
        self.frequency_shift_slider.set(0)
        self.frequency_shift_slider.pack()

        # Plop slider
        self.plop_slider = Tkinter.Scale(self.main_screen, troughcolor="#0000ff", orient=Tkinter.HORIZONTAL, from_=0, to=100, resolution=1, showvalue=True)
        self.plop_slider.set(1)
        self.plop_slider.pack()

        # Echo slider
        self.echo_slider = Tkinter.Scale(self.main_screen, troughcolor="#800080", orient=Tkinter.HORIZONTAL, from_=0, to=10, showvalue=True)
        self.echo_slider.set(0)
        self.echo_slider.pack()

        top_frame.pack()

    def death_preset(self):
        """Sets sliders to presets for death sound."""

        self.frequency_slider.set(2)
        self.frequency_shift_slider.set(0)
        self.plop_slider.set(4)
        self.echo_slider.set(4)

    def pickup_preset(self):
        """Sets sliders to presets for pickup sound."""

        self.frequency_slider.set(3)
        self.frequency_shift_slider.set(3)
        self.plop_slider.set(28)
        self.echo_slider.set(0)

    def jump_preset(self):
        """Sets sliders to presets for jump sound."""

        self.frequency_slider.set(2)
        self.frequency_shift_slider.set(3)
        self.plop_slider.set(0)
        self.echo_slider.set(0)

    def laser_preset(self):
        """Sets sliders to presets for laser sound."""

        pass

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
