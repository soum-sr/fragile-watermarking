import os


BASE_DIR = os.getcwd()

input_folder = os.path.join(BASE_DIR, "input_images")
watermark_folder = os.path.join(BASE_DIR, "watermark_images")
watermark_output_folder = os.path.join(BASE_DIR, "watermark_output")
extracted_watermark_folder = os.path.join(BASE_DIR, "extracted_watermark")
attack_images_folder = os.path.join(BASE_DIR, "attack_images")


# ATTACKS ON WATERMARKED IMAGE
