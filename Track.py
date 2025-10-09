
## Track
import numpy as np
from PIL import Image

START = 0
ROAD = 1
CURB = 2
GRAVEL = 3
WALL = 4
CP1 = 5
CP2 = 6
CP3 = 7
CP4 = 8
FINISH = 9

def colorToNumber(color):
    match color:
        case [0, 255, 255]:
            return START
        case [255, 255, 255]:
            return ROAD
        case [127, 127, 127]:
            return CURB
        case [255, 255, 0]:
            return GRAVEL
        case [0, 0, 255]:
            return WALL
        case [0, 255, 0]:
            return CP1
        case [255, 0, 0]:
            return CP2
        case [255, 0, 255]:
            return CP3
        case [255, 127, 0]:
            return CP4
        case [0, 0, 0]:
            return FINISH
    # shouldn't get here
    return None

def rgbToTrack(rgb):
    height = rgb.shape[0]
    width = rgb.shape[1]
    track_grid = np.zeros(shape = (height, width))
    simple_rgb = rgb.tolist()
    for i in range(height):
        for j in range(width):
            track_grid[i][j] = colorToNumber(simple_rgb[i][j])
    return track_grid

def getStart(track_grid):
    height = track_grid.shape[0]
    width = track_grid.shape[1]
    for i in range(height):
        for j in range(width):
            if track_grid[i][j] == START:
                return i,j
    return None

#
def getLocations(track_grid, type: int):
    locations = set()
    height = track_grid.shape[0]
    width = track_grid.shape[1]
    for i in range(height):
        for j in range(width):
            if track_grid[i][j] == type:
                locations.add((i,j))
    return locations

            
class Track():
    # height
    # width
    # n_checkpoints
    # start_coords
    # track 
                
    def __init__(self, image_path):
        image = Image.open(image_path)
        pixel_data_rgb = np.asarray(image.convert("RGB"))

        self.track_grid = rgbToTrack(pixel_data_rgb)
        self.height = self.track_grid.shape[0]
        self.width = self.track_grid.shape[0]
        self.start_coords = getStart(self.track_grid)

        # checkpoints is an array of sets of points
        # includes finish line as checkpoint n-1
        self.checkpoints = self.getCheckpoints()

        self.n_checkpoints = len(self.checkpoints)

    def getStart(self):
        return self.start_coords
    
    def getCheckpoints(self):
        checkpoints = []

        # start with cp1
        for flavour in [CP1, CP2, CP3, CP4]:
            locations = getLocations(self.track_grid, flavour)
            if len(locations) > 0:
                checkpoints.append(locations)
            else:
                break
        
        locations = getLocations(self.track_grid, FINISH)
        checkpoints.append(locations)
        return checkpoints





        


test = Track("example_mask.png")



print()
