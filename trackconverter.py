
## converts track images from website version to masks

# walls: [60, 120, 240]
# grey grid: [195, 210, 240]
# grey arrow: [195, 195, 195]
# arrow/line intersect: [149, 160, 183]
# grey X: [155, 155, 155]
# grey X middle: [118, 127, 145]

# CP1: [104, 255, 104]
# CP1 grey: [80, 236, 98]

# CP2: [255, 104, 104]
# CP2 grey: [230, 86, 98]

# CP3: [255, 104, 255]
# CP3 grey: [230, 86, 248]

# CP4: [255, 179, 104]
# CP4 grey: [230, 161, 98]


# finish: [0,0,0]
# track: [255, 255, 255]

ROAD = [255, 255, 255]
WALL = [0, 0, 255]
CP1 = [0, 255, 0]
CP2 = [255, 0, 0]
CP3 = [255, 0, 255]
CP4 = [255, 127, 0]
CURB = [127, 127, 127]

import numpy as np
from PIL import Image

name = "canyon_run"
image = Image.open("raw_images/" + str(name) + ".png")

pixel_data_rgb = np.asarray(image.convert("RGB"))

# loop over array of pixels
height = pixel_data_rgb.shape[0]
width = pixel_data_rgb.shape[1]

modified_img = []
for i in range(height):
    row = []
    for j in range(width):
        # replace all the walls with blue
        current = pixel_data_rgb[i][j]
        if np.all(current == [60, 120, 240]):
            row.append(WALL)

        # replace all grey grid
        elif np.all(current == [195, 210, 240]):
            row.append(ROAD)
        
        # replace all grey arrow
        elif np.all(current == [195, 195, 195]):
            row.append(CURB)

        # replace all grey grid/arrow
        elif np.all(current == [149, 160, 183]):
            row.append(CURB)
        
        # replace grey X (not middle)
        elif np.all(current == [155, 155, 155]):
            row.append(ROAD)

        # replace CP1
        elif np.all(current == [104, 255, 104]):
            row.append(CP1)

        # replace CP1/grid
        elif np.all(current == [80, 236, 98]):
            row.append(CP1)
        
        # replace CP2
        elif np.all(current == [255, 104, 104]):
            row.append(CP2)

        # replace CP2/grid
        elif np.all(current == [230, 86, 98]):
            row.append(CP2)
        
        # replace CP3
        elif np.all(current == [255, 104, 255]):
            row.append(CP3)

        # replace CP3/grid
        elif np.all(current == [230, 86, 248]):
            row.append(CP3)

        # replace CP4
        elif np.all(current == [255, 179, 104]):
            row.append(CP4)

        # replace CP4/grid
        elif np.all(current == [230, 161, 98]):
            row.append(CP4)
        else:
            row.append(list(current))

    modified_img.append(row)

np_img = np.array(modified_img)
new_img = Image.fromarray(np_img.astype(np.uint8))
new_img.save("intimages/" + str(name) + ".png")
