


class Color:

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return f"Color: red: {self.red}, green: {self.green}, blue: {self.blue}"
    
    @property
    def color(self):
        return (self.red, self.green, self.blue)

    # INITIALIZERS
    def from_rgb(red, green, blue):
        return Color(red, green, blue)
    
    # CONVERTERS
    def convert_to_cmyk(self):
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
    

RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
YELLOW = Color(255, 255, 0)
CYAN = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)
WHITE = Color(255, 255, 255)
VERY_LIGHT_GRAY = Color(192, 192, 192)
LIGHT_GRAY = Color(192, 192, 192)
MODERATE_LIGHT_GRAY = Color(224, 224, 224)
GRAY = Color(128, 128, 128)
MODERATE_DARK_GRAY = Color(96, 96, 96)
DARK_GRAY = Color(80, 80, 80)
VERY_DARK_GRAY = Color(64, 64, 64)
BLACK = Color(0, 0, 0)