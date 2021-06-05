import os
import time
from PIL import Image
from utils import perform_watermark
from attack_localization import localize_attack
import warnings
warnings.simplefilter("ignore")

input_image = "Lenna.png"
watermark_image = "peppers.png"
watermark_output = "watermarked_Lenna.png"
watermark_modified = "5_marked.png"
extracted_watermark = "extracted_watermark_Lenna.png"
extracted_modified_watermark = "extracted_modified_watermark_Lenna.png"

# image_quality_metrics = perform_watermark('i', input_image, watermark_image, watermark_output, extracted_watermark)


def create_hash(img):
    img = img.resize((20, 20), Image.ANTIALIAS)
    img = img.convert("L")
    pixel_data = list(img.getdata())
    avg_pixel = sum(pixel_data)/len(pixel_data)
    bits = "".join(['1' if (px >= avg_pixel) else '0' for px in pixel_data])
    hex_representation = str(hex(int(bits, 2)))[2:][::-1].upper()
    return hex_representation


def first_phase():
    # Generates watermarked image and extracted watermark
    image_quality_metrics = perform_watermark('i', input_image, watermark_image, watermark_output, extracted_watermark)
    threshold = perform_watermark('e', input_image, watermark_image, watermark_output, extracted_watermark)
    extracted_watermark_img = Image.open(extracted_watermark)
    original_extracted_hash = create_hash(extracted_watermark_img)
    return original_extracted_hash


def second_phase():
    # Generates modified extracted watermark image
    threshold = perform_watermark('e', input_image, watermark_image, watermark_modified, extracted_modified_watermark)
    extracted_modified_watermark_img = Image.open(extracted_modified_watermark)
    modified_extracted_hash = create_hash(extracted_modified_watermark_img)
    return modified_extracted_hash


original_extracted_hash = first_phase()
modified_extracted_hash = second_phase()

if original_extracted_hash == modified_extracted_hash:
    print("No Changes Detected!")
else:
    print("Modification Detected!")
    localize_attack(watermark_output, watermark_modified)
