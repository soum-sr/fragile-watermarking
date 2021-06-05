import numpy as np
from PIL import Image, ImageDraw
import os
from itertools import product


def tile(filename, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(filename)
    w, h = img.size

    grid = list(product(range(0, h-h % d, d), range(0, w-w % d, d)))
    tile_img_list = []
    box_list = []
    for i, j in grid:
        box = (j, i, j+d, i+d)
        box_list.append(box)
        out = f'{name}_{i}_{j}{ext}'
        tile_img = img.crop(box)
        tile_img_list.append(tile_img)
    return tile_img_list, box_list


def create_hash_dict(tile_array):
    hash_dict = {}
    for i, img in enumerate(tile_array):
        img = img.resize((10, 10), Image.ANTIALIAS)
        img = img.convert("L")
        pixel_data = list(img.getdata())
        avg_pixel = sum(pixel_data)/len(pixel_data)
        bits = "".join(['1' if (px >= avg_pixel) else '0' for px in pixel_data])
        hex_representation = str(hex(int(bits, 2)))[2:][::-1].upper()
        hash_dict[i] = hex_representation
    return hash_dict


def draw_rectangle(filename, tamper_location_list):
    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    for box in tamper_location_list:
        draw.rectangle(box, outline='white', width=2)
    img.save('tamper.png')


def localize_attack(image_path, modified_path):
    tile_size = 32

    # Original watermark image

    tile_img_list, box_list = tile(image_path, tile_size)
    original_hash_dict = create_hash_dict(tile_img_list)

    # Modified watermark image

    modified_tile_img_list, modified_box_list = tile(modified_path, tile_size)
    modified_hash_dict = create_hash_dict(modified_tile_img_list)

    tamper_location_list = []
    for i in range(len(tile_img_list)):
        if original_hash_dict[i] != modified_hash_dict[i]:
            tamper_location_list.append(modified_box_list[i])

    draw_rectangle(modified_path, tamper_location_list)


# image_path = "watermarked_baboon.png"
# modified_path = "watermarked_baboon_modified.png"
# localize_attack(image_path, modified_path)
