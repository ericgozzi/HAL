
from PIL import Image, ImageDraw
import math

from ..pixels import Color
from ..pixels import Picture

class Plotter:
    
    def __init__(self, **kwargs):
        self.width = kwargs.get('width', 2000)
        self.height = kwargs.get('height', 2000)
        self.scale = kwargs.get('scale', 100)
        self.x_scale = kwargs.get('x_scale', self.scale)
        self.y_scale = kwargs.get('y_scale', self.scale)
        self.bg_color = kwargs.get('background_color', Color.BLACK)
        
        self.picture = Picture.from_PIL_image(Image.new('RGB', (self.width, self.height), self.bg_color.rgb))

        self.draw = ImageDraw.Draw(self.picture.image)

    @property
    def center_x(self):
        return self.width//2
       
    @property
    def center_y(self):
        return self.height//2
       

    def draw_axes(self, **kwargs):

        color = kwargs.get('color', Color.WHITE)
        color_x = kwargs.get('color_x', color)
        color_y = kwargs.get('color_y', color)

        thickness = kwargs.get('thickness', 2)
        thickness_x = kwargs.get('thickness_x', thickness)
        thickness_y = kwargs.get('thickness_y', thickness)


        self.draw.line((0, self.center_y, self.width, self.center_y), width=thickness, fill=color_x.rgb)
        self.draw.line((self.center_x, 0, self.center_x, self.height), width=thickness, fill=color_y.rgb)





    def plot(self, func, **kwargs):

        color = kwargs.get('color', Color.WHITE)
        thickness = kwargs.get('thickness', 4)

        prev_point = None

        for px in range(self.width):
            x = (px - self.center_x) / self.x_scale
            try:
                y = func(x)
                py = self.center_y - int(y * self.y_scale)
                if 0 <= py < self.height:
                    if prev_point:
                        self.draw.line((prev_point[0], prev_point[1], px, py), fill=color.rgb, width=thickness)
                    prev_point = (px, py)
                else:
                    pre
                    v_point = None
            except:
                prev_point = None


    def plot_parametric(self, func_x, func_y, t_min, t_max, **kwargs):
            
            color = kwargs.get('color', Color.WHITE)
            steps = kwargs.get('steps', 1000)
            thickness = kwargs.get('thickness', 4)

            prev_point = None
            for i in range(steps):
                t = t_min + (t_max - t_min) * i / steps
                try:
                    x = func_x(t)
                    y = func_y(t)
                    px = int(self.center_x + x * self.x_scale)
                    py = int(self.center_y - y * self.y_scale)
                    if 0 <= px < self.width and 0 <= py < self.height:
                        if prev_point:
                            self.draw.line((prev_point[0], prev_point[1], px, py), fill=color.rgb, width=thickness)
                        prev_point = (px, py)
                    else:
                        prev_point = None
                except:
                    prev_point = None


    def plot_points(self, points, **kwargs):
        """Plot a list of (x, y) tuples.
        
        Args:
            points (list): List of (x, y) pairs
            color (str): Point or line color
            radius (int): Size of the dots
            connect (bool): Whether to connect the points with lines
            thickness (int): Line thickness if connecting
        """

        color = kwargs.get('color', Color.WHITE)
        radius = kwargs.get('radius', 4)
        connect = kwargs.get('connect', True)
        thickness = kwargs.get('thickness', 2)

        prev = None
        for x, y in points:
            try:
                px = int(self.center_x + x * self.x_scale)
                py = int(self.center_y - y * self.y_scale)
                if 0 <= px < self.width and 0 <= py < self.height:
                    # Draw a circle for the point
                    self.draw.ellipse((px - radius, py - radius, px + radius, py + radius), fill=color.rgb)
                    # Connect with line if requested
                    if connect and prev:
                        self.draw.line((prev[0], prev[1], px, py), fill=color.rgb, width=thickness)
                    prev = (px, py)
            except:
                prev = None



    def save(self, path='plot.png'):
        self.picture.save(path)


    def show(self):
        self.picture.show()
