from typing import Tuple
from PIL import Image, ImageFont, ImageDraw, ImageOps
import numpy as np
import os
import sys
import math

from numpy.lib.type_check import imag

#source venv/bin/activate

max_width = 128
pallette = [".", "*", "-", "~", "+", "=", "1", "0", "@", "#"]
output_file = "ascii.jpg"

def main():
    try:
        if (len(sys.argv) < 3):
            print("Please provide two arguments, input and output")
            exit()

        input_file = sys.argv[-2]
        output_file = sys.argv[-1]
        ascii_image = create_ascii_image(input_file)
        ascii_image.save(output_file)
    except:
        exit()

def create_ascii_image(input_file: str):
    image_array, image_array_grascale = load_image(input_file)

    ascii_array = image_to_ascii(image_array_grascale)

    ascii_image = ascii_to_image(ascii_array, image_array)
    ascii_image = ascii_image.rotate(-90, Image.NEAREST, expand=1)
    ascii_image = ImageOps.mirror(ascii_image)
    ascii_image.show()
    
    return ascii_image

def ascii_to_image(ascii: list, image_array: list) -> Image:
    width = len(ascii)
    height = len(ascii[0])

    image_width = width*10
    image_height = height*10

    image = Image.new("RGB", (image_width, image_height), (30, 30, 30))

    draw = ImageDraw.Draw(image)

    for x in range(width):
        for y in range(height):
            coordinates = (x*10, y*10)
            ascii_character = ascii[x][y]
            color = tuple(image_array[x][y])
            draw.text(coordinates, ascii_character, color)

    return image

def load_image(file: str) -> Tuple[list, list]:
    with Image.open(file) as image:
        image.thumbnail((max_width, max_width), Image.ANTIALIAS)
        return np.asarray(image).tolist(), np.asarray(image.convert('L')).tolist()

def image_to_ascii(image: list) -> list:
    ascii = [["" for x in range(len(image[0]))] for y in range(len(image))]
    for x in range(len(image)):
        for y in range(len(image[0])):
            symbol = int((len(pallette) - 1) * (image[x][y] / 255))
            ascii[x][y] = pallette[symbol]

    return ascii

def print_array(array):
    for row in array:
        print(row)


if __name__=="__main__":
    main()

