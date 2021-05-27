import math
import itertools
import random
import numpy as np
from PIL import Image
from image_quality import *

# Size = Total pixels of the image, Shuffle_seed = if 0 then no shuffle, else shuffle order


def shuffle_order(size, shuffle_seed):
    order = []
    for i in range(size):
        order.append(i)
    if (shuffle_seed):
        random.seed(shuffle_seed)
        shuffled = random.shuffle(order)
        return order
    else:
        return order


# To encrypt the bits
def encrypt(plain, key):
    cipher = []
    k = 0
    len_key = len(key)
    len_plain = len(plain)
    for i in range(len_plain):
        cipher.append((plain[i] + ord(key[i % len_key])) % 256)
    return cipher


# To decrypt the bits
def decrypt(cipher, key):
    plain = []
    k = 0
    len_key = len(key)
    len_cipher = len(cipher)
    for i in range(len_cipher):
        plain.append((cipher[i] + 256 - ord(key[i % len_key])) % 256)
    return plain


# To read the LSB
def readLSB(image, width, binary, order):
    bit = []
    px = image.load()
    k = 0
    cur = 0
    for pos in order:
        i = pos / width
        j = pos % width
        if (binary):
            cur |= (px[i % image.width, j % image.height] & 1) << k
        else:
            cur |= (px[i % image.width, j % image.height][0] & 1) << k
        k += 1
        if (k >= 8):
            bit.append(cur)
            k = 0
            cur = 0
    if (k > 0):
        bit.append(cur)
    return bit


# To insert lsb
def insert_lsb(inputpath, watermarkpath, outputpath):
    cover = Image.open(inputpath)
    # Convert to bnw
    watermark = Image.open(watermarkpath).convert("1")
    output = Image.new(cover.mode, cover.size)
    # To load the pixels into memory
    px_cover = cover.load()
    px_watermark = watermark.load()
    px_output = output.load()
    plain = readLSB(watermark, cover.width, 1, shuffle_order(cover.width * cover.height, 0))
    # Encrypt the pixels with the help of user input key
    key = "qwertyuiop"
    cipher = encrypt(plain, key)

    k = 0
    cur = 0
    mod = watermark.width * watermark.height
    seed = 0
    key_size = len(key)
    for i in range(key_size):
        seed += ord(key[i])
    positions = shuffle_order(cover.width * cover.height, seed)
    for pos in positions:
        i = pos / cover.width
        j = pos % cover.width
        p = list(px_cover[i, j])
        p[0] = (p[0] & 0b11111110) | ((cipher[int(k / 8)] >> (k % 8)) & 1)
        k = (k + 1) % mod
        px_output[i, j] = tuple(p)
    output.save(outputpath)


def extract_lsb(inputpath, outputpath):
    cover = Image.open(inputpath)
    lsb = Image.new("1", cover.size)
    px_cover = cover.load()
    px_lsb = lsb.load()

    key = "qwertyuiop"
    seed = 0
    key_size = len(key)
    for i in range(key_size):
        seed += ord(key[i])
    cipher = readLSB(cover, cover.width, 0, shuffle_order(cover.width * cover.height, seed))
    plain = decrypt(cipher, key)

    k = 0
    cur = 0
    positions = shuffle_order(cover.width * cover.height, 0)
    for pos in positions:
        i = pos / cover.width
        j = pos % cover.width
        px_lsb[i, j] = ((plain[int(k / 8)] >> (k % 8)) & 1)
        k = (k + 1)
    lsb.save(outputpath)


def perform_watermark(task, input_file, watermark_file, watermark_output_path, extracted_watermark_path):
    if task == 'i':
        print("Performing Insert watermark")
        insert_lsb(input_file, watermark_file, watermark_output_path)
        print("Watermark inserted")

        input_image = Image.open(input_file)
        input_image = np.array(input_image)
        watermarked_image = Image.open(watermark_output_path)
        watermarked_image = np.array(watermarked_image)

        mse_val = mse(input_image, watermarked_image)
        rmse_val = rmse(input_image, watermarked_image)

        psnr_val = psnr(input_image, watermarked_image)
        uqi_val = uqi(input_image, watermarked_image)
        ssim_val = ssim(input_image, watermarked_image)
        ergas_val = ergas(input_image, watermarked_image)
        scc_val = scc(input_image, watermarked_image)
        rase_val = rase(input_image, watermarked_image)
        sam_val = sam(input_image, watermarked_image)
        vifp_val = vifp(input_image, watermarked_image)
        msssim_val = msssim(input_image, watermarked_image)
        psnrb_val = psnrb(input_image, watermarked_image)

        image_quality_metrics = {"mse": mse_val,
                                 "rmse": rmse_val,
                                 "psnr": psnr_val,
                                 "uqi": uqi_val,
                                 "ssim": ssim_val[0],
                                 "ergas": ergas_val,
                                 "scc": scc_val,
                                 "rase": rase_val,
                                 "sam": sam_val,
                                 "vifp": vifp_val,
                                 "msssim": msssim_val,
                                 "psnrb": psnrb_val}

        return image_quality_metrics
    else:
        print("Extracting...")
        extract_lsb(watermark_output_path, extracted_watermark_path)
        print("Extracted!!")
