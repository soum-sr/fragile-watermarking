import os
import time
import pandas as pd
from PIL import Image
from utils import perform_watermark

start_time = time.time()

BASE_DIR = os.getcwd()

input_folder = os.path.join(BASE_DIR, "input_images")
watermark_folder = os.path.join(BASE_DIR, "watermark_images")
watermark_output_folder = os.path.join(BASE_DIR, "watermark_output")
extracted_watermark_folder = os.path.join(BASE_DIR, "extracted_watermark")
attack_images_folder = os.path.join(BASE_DIR, "attack_images")

observations_columns = ["input_file",
                        "watermark_file",
                        "mse",
                        "rmse",
                        "psnr",
                        "uqi",
                        "ssim",
                        "ergas",
                        "scc",
                        "rase",
                        "sam",
                        "vifp",
                        "msssim",
                        "psnrb"]

observation_df = pd.DataFrame(columns=observations_columns)

for input_file in os.listdir(input_folder):
    for watermark_file in os.listdir(watermark_folder):
        if input_file != watermark_file:
            input_path = os.path.join(input_folder, input_file)
            watermark_path = os.path.join(watermark_folder, watermark_file)
            out_files = input_file.split('.')[0] + '_' + watermark_file
            watermark_output_path = os.path.join(watermark_output_folder, "watermarked_" + out_files)
            extracted_watermark_path = os.path.join(extracted_watermark_folder, "extracted_" + out_files)

            file_dict = {"input_file": input_file, "watermark_file": watermark_file}
            image_quality_metrics = perform_watermark_metrics('i', input_path, watermark_path, watermark_output_path, extracted_watermark_path)

            row = {**file_dict, **image_quality_metrics}
            observation_df = observation_df.append(row, ignore_index=True)

            # extracting watermark from watermarked images
            perform_watermark_metrics('e', input_path, watermark_path, watermark_output_path, extracted_watermark_path)
observation_df.to_csv('observation.csv', index=False)
end_time = time.time()
print("Total time taken: ", int(end_time-start_time))
