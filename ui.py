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

        SLIDER_WIDTH (int): The width of the sliders in pixels.
        SLIDER_HEIGHT (int): The height of the sliders in pixels.
        BUTTON_WIDTH (int): The width of the buttons in text units (Because they contain text).
        BUTTON_HEIGHT (int): The height of the buttons in text units (Becuase they contain text).

        button_parent (widget): The parent of the buttons. (Can be a frame, the main screen etc.)
        slider_parent (widget): The parent of the sliders. (Can be a frame, the main screen etc.)

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

    SLIDER_WIDTH = 400
    SLIDER_HEIGHT = 30
    BUTTON_WIDTH = 25
    BUTTON_HEIGHT = 5

    button_parent = main_screen
    slider_parent = main_screen

    title_text = None

    volume_slider = None
    frequency_slider = None
    frequency_shift_slider = None
    echo_slider = None
    plop_slider = None

    death_preset_button = None
    jump_preset_button = None
    pickup_preset_button = None
    laser_preset_button = None

    def __init__(self):
        """Initialises and sets up the user interface"""

        self.main_screen = Tkinter.Tk()
        self.main_screen.minsize(0, 600)

        self.init_ui()

    def init_ui(self):
        """Initialise ui elements."""

        # Title message.
        self.title_text = Tkinter.Label(font=("Courier", 15), justify=Tkinter.CENTER, text="Sound Generation Tool by Louis Foy and Mango Gilchrist. \n Use the sliders below to choose the colour of your sound! \n"
                                                                                           "Preset sounds are also available by clicking on the buttons below.")
        self.title_text.grid(row=0, columnspan=4)

        # Preset sound buttons.
        self.death_preset_button = Tkinter.Button(self.button_parent, height=self.BUTTON_HEIGHT, width=self.BUTTON_WIDTH, text="Death Sound", command=lambda: self.death_preset())
        self.death_preset_button.grid(row=2, column=0)

        self.jump_preset_button = Tkinter.Button(self.button_parent, height=self.BUTTON_HEIGHT, width=self.BUTTON_WIDTH, text="Jump Sound", command=lambda: self.jump_preset())
        self.jump_preset_button.grid(row=2, column=1)

        self.pickup_preset_button = Tkinter.Button(self.button_parent, height=self.BUTTON_HEIGHT, width=self.BUTTON_WIDTH, text="Pickup Sound", command=lambda: self.pickup_preset())
        self.pickup_preset_button.grid(row=2, column=2)

        self.laser_preset_button = Tkinter.Button(self.button_parent, height=self.BUTTON_HEIGHT, width=self.BUTTON_WIDTH, text="Laser Sound", command=lambda: self.laser_preset())
        self.laser_preset_button.grid(row=2, column=3)

        # Play/Save buttons
        self.play_preview = Tkinter.Button(self.button_parent, height=self.BUTTON_HEIGHT, width=self.BUTTON_WIDTH * 2, text="Play Sound")
        self.play_preview.grid(row=1, column=0, columnspan=2, sticky=Tkinter.W)

        self.save_sound = Tkinter.Button(self.button_parent, height=self.BUTTON_HEIGHT, width=self.BUTTON_WIDTH * 2, text="Save Sound")
        self.save_sound.grid(row=1, column=2, columnspan=2, sticky=Tkinter.E)

        # Volume slider
        self.volume_slider = Tkinter.Scale(self.slider_parent, length=self.SLIDER_WIDTH, width=self.SLIDER_HEIGHT, troughcolor="#FFFF00", orient=Tkinter.HORIZONTAL, from_=0, to=100, showvalue=True)
        self.volume_slider.set(100)
        self.volume_slider.grid(row=3, columnspan=4)

        # Frequency slider
        self.frequency_slider = Tkinter.Scale(self.slider_parent, length=self.SLIDER_WIDTH, width=self.SLIDER_HEIGHT, troughcolor="#000000", orient=Tkinter.HORIZONTAL, from_=0.1, to=5.0, resolution=0.1, showvalue=True)
        self.frequency_slider.set(1)
        self.frequency_slider.grid(row=4, columnspan=4)

        # Frequency shift slider
        self.frequency_shift_slider = Tkinter.Scale(self.slider_parent, length=self.SLIDER_WIDTH, width=self.SLIDER_HEIGHT, troughcolor="#ff0000", orient=Tkinter.HORIZONTAL, from_=0, to=5.0, resolution=0.1, showvalue=True)
        self.frequency_shift_slider.set(0)
        self.frequency_shift_slider.grid(row=5, columnspan=4)

        # Plop slider
        self.plop_slider = Tkinter.Scale(self.slider_parent, length=self.SLIDER_WIDTH, width=self.SLIDER_HEIGHT, troughcolor="#0000ff", orient=Tkinter.HORIZONTAL, from_=0, to=100, resolution=1, showvalue=True)
        self.plop_slider.set(1)
        self.plop_slider.grid(row=6, columnspan=4)

        # Echo slider
        self.echo_slider = Tkinter.Scale(self.slider_parent, length=self.SLIDER_WIDTH, width=self.SLIDER_HEIGHT, troughcolor="#800080", orient=Tkinter.HORIZONTAL, from_=0, to=10, showvalue=True)
        self.echo_slider.set(0)
        self.echo_slider.grid(row=7, columnspan=4)

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

        self.frequency_slider.set(2.5)
        self.frequency_shift_slider.set(2)
        self.plop_slider.set(80)
        self.echo_slider.set(0)

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
