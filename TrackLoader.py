from PIL import Image
import cv2
import numpy as np

image_path = "example_mask.png" 

image = Image.open(image_path)

pixel_data_rgb = np.asarray(image.convert("RGB"))






print(pixel_data_rgb.shape)


print(getStart(pixel_data_rgb))