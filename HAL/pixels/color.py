


class Color:
    """
    # Color Class

    The `Picture`class represent images.
    """

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return f"Color: red: {self.red}, green: {self.green}, blue: {self.blue}"

    @property
    def color(self) -> tuple:
        """
        A 3-values tuple representing the color in RGB.
        """
        return (self.red, self.green, self.blue)

    # INITIALIZERS
    @classmethod
    def from_rgb(cls, red: int, green: int, blue: int):
        """
        Initiliaze the color from a RGB values.

        Args:
            red (int): The red value in the range (0 - 255)
            green (int): The green value in the range (0 - 255)
            blue (int): The blue value in the range (0 - 255)

        Returns
            Color: A color object
        """
        return cls(red, green, blue)

    # CONVERTERS
    def convert_to_cmyk(self) -> tuple:
        """
        Convertes the color to the cmyk format.

        Returns:
            tuple(4): A 4 dimensional color with (C, M, Y, K) values.
        """
        r = self.red
        g = self.green
        b = self.blue
        # Find the Key (Black) value
        k = 1 - max(r, g, b)

        if k < 1:  # If not black
            c = (1 - r - k) / (1 - k)
            m = (1 - g - k) / (1 - k)
            y = (1 - b - k) / (1 - k)
        else:  # If black
            c = m = y = 0

        # Convert CMYK to percentage (0-100 scale)
        return (c * 100, m * 100, y * 100, k * 100)




    def as_integer(self):
        integer = self.red + self.green + self.blue
        return integer


    @classmethod
    def from_integer(cls, integer: int):
        red, green, blue = 0, 0, 0
        if integer > 255:
            red = 255
            integer -= 255
        else:
            red = integer
            return Color(red, green, blue)
        if integer > 255:
            green = 255
            integer -= 255
        else:
            green = integer
            return Color(red, green, blue)

        if integer > 255:
            raise ValueError("Integer too big")
        else:
            blue = integer
            return Color(red, green, blue)


    def as_char(self):
        """
        Decodes a single character from an RGB color.
        """
        if not (isinstance(self.color, tuple) and len(self.color) == 3):
            raise ValueError("Color must be a tuple of (R, G, B).")

        r, g, b = self.color
        if not (0 <= r <= 255):
            raise ValueError("Red channel must be between 0 and 255.")
        return chr(g)

    @classmethod
    def from_char(cls, char: str):
        """
        Encodes a single character to an RGB color.
        """
        if len(char) != 1:
            raise ValueError("Input must be a single character.")

        ascii_val = ord(char)
        if not 0 <= ascii_val <= 255:
            raise ValueError("Character out of ASCII range.")

        # Encode ASCII value into the Red channel
        return cls(0, ascii_val, 0)

    @classmethod
    def constants(cls):

        #: Pure red color (RGB: 255, 0, 0)
        cls.RED = cls(255, 0, 0)

        #: Pure green color (RGB: 0, 255, 0)
        cls.GREEN = cls(0, 255, 0)

        #: Pure blue color (RGB: 0, 0, 255)
        cls.BLUE = cls(0, 0, 255)

        #: Yellow color, a mix of red and green (RGB: 255, 255, 0)
        cls.YELLOW = cls(255, 255, 0)

        #: Cyan color, a mix of green and blue (RGB: 0, 255, 255)
        cls.CYAN = cls(0, 255, 255)

        #: Magenta color, a mix of red and blue (RGB: 255, 0, 255)
        cls.MAGENTA = cls(255, 0, 255)

        #: Pure white color (RGB: 255, 255, 255)
        cls.WHITE = cls(255, 255, 255)

        #: Very light gray, slightly darker than white (RGB: 192, 192, 192)
        cls.VERY_LIGHT_GRAY = cls(192, 192, 192)

        #: Light gray color (RGB: 192, 192, 192)
        cls.LIGHT_GRAY = cls(192, 192, 192)

        #: Moderate light gray, between light gray and white (RGB: 224, 224, 224)
        cls.MODERATE_LIGHT_GRAY = cls(224, 224, 224)

        #: Neutral gray, midway between black and white (RGB: 128, 128, 128)
        cls.GRAY = cls(128, 128, 128)

        #: Moderate dark gray, slightly darker than neutral gray (RGB: 96, 96, 96)
        cls.MODERATE_DARK_GRAY = cls(96, 96, 96)

        #: Dark gray, significantly darker than neutral gray (RGB: 80, 80, 80)
        cls.DARK_GRAY = cls(80, 80, 80)

        #: Very dark gray, close to black but not completely black (RGB: 64, 64, 64)
        cls.VERY_DARK_GRAY = cls(64, 64, 64)

        #: Pure black color (RGB: 0, 0, 0)
        cls.BLACK = cls(0, 0, 0)




def string_to_colors(text: str) -> list[Color]:
    """Encodes a string into a list of RGB colors."""
    return [Color.from_char(c) for c in text]


def colors_to_string(colors) -> str:
    """Decodes a string from a list of RGB colors."""
    return ''.join(color.as_char() for color in colors)
