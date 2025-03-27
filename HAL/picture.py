import math

import numpy as np

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageOps
from PIL import ImageEnhance
from PIL import ImageChops

from HAL.color import Color
from HAL.color import BLACK
from HAL.color import WHITE


class Picture:

    def __init__(self, image):
        self.image = image

    # Constructors
    def from_file_path(image_path):
        image = Image.open(image_path)
        return Picture(image)
    
    def from_PIL_image(image):
        return Picture(image)


    @property
    def size(self):
        return self.image.size
    
    @property
    def width(self):
        return self.image.width
    
    @property
    def height(self):
        return self.image.height   
    
    @property
    def entropy(self):
        return self.image.entropy()

    @property
    def mode(self):
        return self.image.mode
    
    @property
    def red_channel(self):
        r_values = self.image.split()[0]
        red_image = Image.merge("RGB", (r_values, Image.new("L", self.image.size, 0), Image.new("L", self.image.size, 0)))
        return Picture.from_PIL_image(red_image)

    @property
    def green_channel(self):
        g_values = self.image.split()[1]
        green_image = Image.merge("RGB", (Image.new("L", self.image.size, 0), g_values, Image.new("L", self.image.size, 0)))
        return Picture.from_PIL_image(green_image)

    @property
    def blue_channel(self):
        b_values = self.image.split()[2]
        blue_image = Image.merge("RGB", (Image.new("L", self.image.size, 0), Image.new("L", self.image.size, 0), b_values))
        return Picture.from_PIL_image(blue_image)


    # General methods

    def show(self):
        self.image.show()

    def save(self, output_path):
        self.image.save(output_path)

    def copy(self):
        return Picture.from_PIL_image(self.image.copy())

    def convert_to_grayscale(self):
        self.image = self.image.convert('L') 
    
    def convert_to_rgb(self):
        self.image = self.image.convert('RGB')

    def convert_to_rgba(self):
        self.image = self.image.convert('RGBA')

    def adjust_brightness(self, value: float):
        # Adjust the exposure (1.0 = original, >1.0 = brighter, <1.0 = darker)
        enhancer = ImageEnhance.Brightness(self.image)
        enhanced_image = enhancer.enhance(value)
        self.image = enhanced_image

    def adjust_contrast(self, value: float):
        enhancer = ImageEnhance.Contrast(self.image)
        enhanced_image = enhancer.enhance(value)
        self.image = enhanced_image

    def adjust_sharpness(self, value: float):
        enhancer = ImageEnhance.Sharpness(self.image)
        enhanced_image = enhancer.enhance(value)
        self.image = enhanced_image

    def adjust_saturation(self, value: float):
        enhancer = ImageEnhance.Color(self.image)
        enhanced_image = enhancer.enhance(value)
        self.image = enhanced_image


    # Geometry

    def rotate(self, angle):
        self.image = self.image.rotate(angle)

    def resize(self, width, height, **kwargs):

        keep_aspect_ratio = kwargs.get("keep_aspect_ratio", False)
        crop = kwargs.get("crop", False)

        if keep_aspect_ratio and not crop:
            self.image = ImageOps.cover(self.image, (width, height))
        if (keep_aspect_ratio and crop) or crop:
            self.image = ImageOps.fit(self.image, (width, height))
        if not keep_aspect_ratio and not crop:
            self.image = self.image.resize((width, height)) 

    def crop(self, left_margin, top_margin, right_margin, bottom_margin):
        width, height = self.size
        self.image = self.image.crop((left_margin, top_margin, width - right_margin, height - bottom_margin))

    def flip_horizontal(self):
        self.image = ImageOps.mirror(self.image)

    def flip_vertical(self):
        self.image = ImageOps.flip(self.image)



    def get_main_colors(self, num_colors) -> list:
        # Convert image to "P" mode (palette-based) with an adaptive palette
        image = self.image.convert("P", palette=Image.ADAPTIVE, colors=num_colors)

        # Get the palette (a list of RGB values, where every 3 values are an (R, G, B) triplet)
        palette = image.getpalette()[:num_colors * 3]  # Only get requested number of colors

        # Convert flat list to list of RGB tuples
        colors = [tuple(palette[i:i+3]) for i in range(0, len(palette), 3)]
        colors = [Color(c[0], c[1], c[2]) for c in colors]
        return colors
    
    def get_color_palette(self, num_colors):
        colors = self.get_main_colors(num_colors)
        color_pictures = []
        for color in colors:
            color_pictures.append(Picture.from_PIL_image(Image.new('RGB', (100, 100), color.color)))
        palette = create_grid_of_pictures(color_pictures, grid_size=(num_colors, 1), image_size=(100, 100))
        return palette


    # Dithering methods

    def dither_halftone(self, **kwargs):
        # Kwargs
        dot_color = kwargs.get('dot_color', BLACK)
        background_color = kwargs.get('background_color', WHITE)
        dot_spacing = kwargs.get('dot_spacing', 12)
        dot_size = kwargs.get('dot_size', 8)

        # Open image and convert to grayscale
        self.convert_to_grayscale()
        width, height = self.size
        halftone = Image.new('RGB', (width, height), background_color.color)
        draw = ImageDraw.Draw(halftone)
        
        # Process image in a grid pattern
        for y in range(0, height, dot_spacing):
            for x in range(0, width, dot_spacing):
                # Get pixel brightness (0-255, where 0 is black and 255 is white)
                brightness = self.image.getpixel((x, y))
                # Scale dot size based on brightness (darker areas have larger dots)
                radius = (1 - brightness / 255) * dot_size / 2
                
                if radius > 0:
                    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=dot_color.color)
      
        self.image =  halftone


    def dither_ordered(self, **kwargs):
        # Kwargs
        matrix_size = kwargs.get('matrix_size', 8)
        scale_factor = kwargs.get('scale_factor', 5)
        color = kwargs.get('color', WHITE)
        background_color = kwargs.get('background_color', BLACK)

        # Bayer matrices of different sizes
        bayer_matrices = {
            2: np.array([[0, 2], [3, 1]]) / 4.0,
            4: np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0,
            8: np.array([
                [0, 32, 8, 40, 2, 34, 10, 42],
                [48, 16, 56, 24, 50, 18, 58, 26],
                [12, 44, 4, 36, 14, 46, 6, 38],
                [60, 28, 52, 20, 62, 30, 54, 22],
                [3, 35, 11, 43, 1, 33, 9, 41],
                [51, 19, 59, 27, 49, 17, 57, 25],
                [15, 47, 7, 39, 13, 45, 5, 37],
                [63, 31, 55, 23, 61, 29, 53, 21]
            ]) / 64.0
        }
        
        if matrix_size not in bayer_matrices:
            raise ValueError("Unsupported matrix size. Choose from 2, 4, or 8.")
        
        bayer_matrix = bayer_matrices[matrix_size]
        threshold_map = (bayer_matrix * 255).astype(np.uint8)
        
        # Open image and convert to grayscale
        self.convert_to_grayscale()
        width, height = self.image.size
        pixels = np.array(self.image, dtype=np.uint8)

        # Convert image to RGB to sore colore pixels
        color_pixels = np.zeros((height, width, 3), dtype=np.uint8)

        # Apply dithering
        for y in range(0, height, scale_factor):
            for x in range(0, width, scale_factor):
                threshold = threshold_map[(y // scale_factor) % matrix_size, (x // scale_factor) % matrix_size]
                color_pixels[y:y+scale_factor, x:x+scale_factor] = color.color if pixels[y, x] > threshold else background_color.color
        
        dithered_image = Image.fromarray(color_pixels, mode='RGB')
        self.image =  dithered_image


    def dither_floyd_steinberg(self, **kwargs):
        scale_factor = kwargs.get('scale_factor', 3)

        self.convert_to_grayscale()
        pixels = np.array(self.image, dtype=np.float32)
        height, width = pixels.shape
        
        scaled_height = int(height / scale_factor)
        scaled_width = int(width / scale_factor)
        scaled_image = Image.fromarray(pixels.astype(np.uint8)).resize((scaled_width, scaled_height), Image.NEAREST)
        pixels = np.array(scaled_image, dtype=np.float32)
        
        for y in range(scaled_height):
            for x in range(scaled_width):
                old_pixel = pixels[y, x]
                new_pixel = 255 if old_pixel > 127 else 0
                pixels[y, x] = new_pixel
                quant_error = old_pixel - new_pixel
                
                if x < scaled_width - 1:
                    pixels[y, x + 1] += quant_error * (7 / 16)
                if y < scaled_height - 1:
                    if x > 0:
                        pixels[y + 1, x - 1] += quant_error * (3 / 16)
                    pixels[y + 1, x] += quant_error * (5 / 16)
                    if x < scaled_width - 1:
                        pixels[y + 1, x + 1] += quant_error * (1 / 16)
        
        dithered_image = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8), mode='L')
        dithered_image = dithered_image.resize((width, height), Image.NEAREST)
        self.image = dithered_image


    def binarize(self, **kwargs):

        threshold = kwargs.get("threshold", 128)
        grayscale = kwargs.get("grayscale", True)
        color = kwargs.get("color", None)

        if grayscale or color:
            self.convert_to_grayscale()

        binarized_image = self.image.point(lambda p: 255 if p > threshold else 0)
        self.image = binarized_image

        if color:
            self.convert_to_rgb()
            pixels = self.image.load()
            for y in range(self.image.height):
                for x in range(self.image.width):
                    if pixels[x, y] == (0, 0, 0):
                        pixels[x, y] = color.color


    def create_alpha_mask(self):
        binarized_image = self.copy()
        self.convert_to_rgba()
        for y in range(self.image.height):
            for x in range(self.image.width):
                pixel_value = binarized_image.image.getpixel((x, y))
                if pixel_value == 0:
                    self.image.putpixel((x, y), (255, 255, 255, 0))
                else:
                    self.image.putpixel((x, y), (0, 0, 0, 1))
        self.convert_to_grayscale()

    def apply_alpha_mask(self, mask):
        self.image.putalpha(mask.image)

                    

    # Filters
    def blur(self, radius: float):
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))

    def invert_colors(self):
        self.image = ImageOps.invert(self.image)
    
    def apply_color(self, color):
        color_filter = Image.new("RGB", self.image.size, color.color)
        self.image = ImageChops.multiply(self.image, color_filter)





# Blendings
def blend_images(image1: Picture, image2: Picture, **kwargs) -> Picture:
    if image1.size != image2.size:
        raise ValueError("Images must have the same size.")
    if image1.mode != image2.mode:
        raise ValueError("Images must have the same mode.")
    alpha = kwargs.get('alpha', 0.5)
    pil_image = Image.blend(image1.image, image2.image, alpha)
    return Picture.from_PIL_image(pil_image)



def create_grid_of_pictures(pictures: list[Picture], **kwargs) -> Picture:
    
    grid_size = kwargs.get('grid_size', (math.ceil(math.sqrt(len(pictures))), math.ceil(math.sqrt(len(pictures)))))
    image_size = kwargs.get('image_size', (720, 720))


    cols, rows = grid_size
    collage_width = cols * image_size[0]
    collage_height = rows * image_size[1]
    
    collage = Image.new('RGB', (collage_width, collage_height))
    
    for index, picture in enumerate(pictures):
        if index >= cols * rows:
            break
        
        img = picture.image
        img.thumbnail(image_size)  # Maintain aspect ratio while resizing
        
        # Create a blank image with the target size and paste the resized image at the center
        temp_img = Image.new('RGB', image_size, (255, 255, 255))  # White background
        x_offset = (image_size[0] - img.size[0]) // 2
        y_offset = (image_size[1] - img.size[1]) // 2
        temp_img.paste(img, (x_offset, y_offset))
        
        x_offset = (index % cols) * image_size[0]
        y_offset = (index // cols) * image_size[1]
        
        collage.paste(temp_img, (x_offset, y_offset))
    
    return Picture.from_PIL_image(collage)

def superimpose_pictures(picture_1, picture_2):
    picture_1 = picture_1.copy()
    picture_1.image.paste(picture_2.image, (0, 0), picture_2.image)
    return picture_1