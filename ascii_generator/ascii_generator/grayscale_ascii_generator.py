from typing import Tuple
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import sys


class AsciiImageGenerator():
    def __init__(self):
        self.max_width = 128
        self.pallette = [".", "*", "-", "~", "+", "=", "1", "0", "@", "#"]
        self.dynamic_color = False
        self.font_color = (255, 255, 255)
        self.background_color = (30, 30, 30)

        self.image_array = None
        self.image_array_grayscale = None
        self.ascii_array = None

        self.input_image = None
        self.output_image = None

    def create_ascii_image(self) -> str:
        self.ascii_array = self.image_to_ascii(self.image_array_grayscale)

        ascii_image = self.ascii_to_image(self.ascii_array, self.image_array)
        ascii_image = ascii_image.rotate(-90, Image.NEAREST, expand=1)
        ascii_image = ImageOps.mirror(ascii_image)

        self.output_image = ascii_image

        self.save_image("ascii.jpg")

        return "ascii.jpg"

    def ascii_to_image(self, ascii: list, image_array: list) -> Image:
        width = len(ascii)
        height = len(ascii[0])

        image_width = width*10
        image_height = height*10

        image = Image.new("RGB", (image_width, image_height), self.background_color)

        draw = ImageDraw.Draw(image)

        for x in range(width):
            for y in range(height):
                coordinates = (x*10, y*10)
                ascii_character = ascii[x][y]
                if (self.dynamic_color):
                    color = tuple(image_array[x][y])
                else:
                    color = self.font_color
                
                draw.text(coordinates, ascii_character, color)

        return image
    
    def get_ascii_text(self):
        ascii = ""
        
        if(not self.ascii_array):
            return ascii
        
        for row in self.ascii_array:
            ascii = ascii + ''.join(row) + "\n"
        
        return ascii

    def save_image(self, file: str):
        if self.output_image:
            self.output_image.save(file)

    def image_to_ascii(self, image: list) -> list:
        ascii = [["" for x in range(len(image[0]))] for y in range(len(image))]
        for x in range(len(image)):
            for y in range(len(image[0])):
                symbol = int((len(self.pallette) - 1) * (image[x][y] / 255))
                ascii[x][y] = self.pallette[symbol]

        return ascii

    def set_input_image(self, file: str):
        with Image.open(file) as image:
            self.input_image = image
            image.thumbnail((self.max_width, self.max_width), Image.ANTIALIAS)
            self.image_array = np.asarray(image).tolist()
            self.image_array_grayscale = np.asarray(image.convert('L'))

    def set_pallette(self, pallette: list):
        self.pallette = pallette
        
    def set_dynamic_color(self, dynamic_color: bool):
        self.dynamic_color = dynamic_color
        
    def set_font_color(self, font_color: Tuple[int, int, int, int]):
        self.font_color = font_color
        
    def set_background_color(self, background_color: Tuple[int, int, int, int]):
        self.background_color = background_color