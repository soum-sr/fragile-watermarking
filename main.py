import os
import pandas as pd
from PIL import Image
from utils import perform_watermark


BASE_DIR = os.getcwd()

input_folder = os.path.join(BASE_DIR, "input_images")
watermark_folder = os.path.join(BASE_DIR, "watermark_images")
watermark_output_folder = os.path.join(BASE_DIR, "watermark_output")
extracted_watermark_folder = os.path.join(BASE_DIR, "extracted_watermark")
attack_images_folder = os.path.join(BASE_DIR, "attack_images")


def convert_bnw(filename, input_folder, output_folder):
    input_path = os.path.join(input_folder, filename)
    img = Image.open(input_path)
    img = img.convert("1")
    output_path = os.path.join(output_folder, filename)
    img.save(output_path)
    print("File saved: ", output_path)


# Convert all input images to BNW(to use them as watermark images)
for file in os.listdir(input_folder):
    convert_bnw(file, input_folder, watermark_folder)

observation_df = pd.DataFrame(columns=["input_file", "watermark_file", "psnr_value"])

for input_file in os.listdir(input_folder):
    for watermark_file in os.listdir(watermark_folder):
        if input_file != watermark_file:
            input_path = os.path.join(input_folder, input_file)
            watermark_path = os.path.join(watermark_folder, watermark_file)
            watermark_output_path = os.path.join(watermark_output_folder, "watermarked_" + input_file)
            extracted_watermark_path = os.path.join(extracted_watermark_folder, "extracted_" + watermark_file)

            psnr_val = perform_watermark('i', input_path, watermark_path, watermark_output_path, extracted_watermark_path)
            row = {"input_file": input_file, "watermark_file": watermark_file, "psnr_value": psnr_val}
            observation_df = observation_df.append(row, ignore_index=True)

observation_df.to_csv('observation.csv', index=False)
