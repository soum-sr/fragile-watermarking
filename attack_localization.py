import numpy as np
from PIL import Image
import os
from itertools import product


def tile(filename, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(filename)
    w, h = img.size

    grid = list(product(range(0, h-h % d, d), range(0, w-w % d, d)))
    tile_img_list = []
    for i, j in grid:
        box = (j, i, j+d, i+d)
        out = f'{name}_{i}_{j}{ext}'
        tile_img = img.crop(box)
        tile_img_list.append(tile_img)
    return tile_img_list


image_path = "watermarked_baboon.png"
image = Image.open(image_path)
image = np.array(image)


tile_img_list = tile(image_path, 128)
