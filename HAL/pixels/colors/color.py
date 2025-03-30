


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
    def from_rgb(red: int, green: int, blue: int):
        """
        Initiliaze the color from a RGB values.

        Args:
            red (int): The red value in the range (0 - 255)
            green (int): The green value in the range (0 - 255)
            blue (int): The blue value in the range (0 - 255)

        Returns
            Color: A color object
        """
        return Color(red, green, blue)
    
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
    
