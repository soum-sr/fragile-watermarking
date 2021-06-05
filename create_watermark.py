import os
from PIL import Image

BASE_DIR = os.getcwd()
input_folder = os.path.join(BASE_DIR, "input_images")
watermark_folder = os.path.join(BASE_DIR, "watermark_images")
watermark_output_folder = os.path.join(BASE_DIR, "watermark_output")
extracted_watermark_folder = os.path.join(BASE_DIR, "extracted_watermark")
attack_images_folder = os.path.join(BASE_DIR, "attack_images")


def convert_bnw(filename, input_folder, output_folder):
    input_path = os.path.join(input_folder, filename)
    img = Image.open(input_path)
    img = img.convert("L")
    output_path = os.path.join(output_folder, filename)
    img.save(output_path)
    print("File saved: ", output_path)


# Convert all input images to BNW(to use them as watermark images)
for file in os.listdir(input_folder):
    convert_bnw(file, input_folder, watermark_folder)
