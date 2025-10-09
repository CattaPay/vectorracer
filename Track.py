
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

# algorithm to determine which cells are passed thru
def bresenham(start, end):
    x0, y0 = start
    x1, y1 = end
    cells = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        cells.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return cells
            
class Track():
    # height
    # width
    # n_checkpoints
    # start_coords
    # track 

    # valid_moves 
                
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

        # hashmap of move -> {False,True}
        # 
        self.valid_moves = {}

        # list of checkpoints crossed in a given move
        self.checkpoints_crossed = {}

    def getStart(self):
        return self.start_coords
    
    def getCell(self,position):
        return self.track_grid[position[0]][position[1]]
    
    def isWall(self,position):
        return self.getCell(position) == WALL
    
    def checkForWalls(self, path):
        for position in path:
            if self.isWall(position):
                return True
        return False

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
    
    def checkValid(self, start, end):
        key = (start[0], start[1], end[0], end[1])

        # if it's been checked, return value
        if key in self.valid_moves:
            return self.valid_moves[key]
        
        # otherwise, check path
        path = bresenham(start, end)
        isValid = not self.checkForWalls(path)

        # update hashmap
        self.valid_moves[key] = isValid
        return isValid
    
    def checkCheckpoint(self, start, end):
        key = (start[0], start[1], end[0], end[1])

        # if it's been checked, return value
        if key in self.checkpoints_crossed:
            return self.checkpoints_crossed[key]
        
        # otherwise, check path
        path = bresenham(start, end)
        cp_set = set()
        for position in path:
            val = self.getCell(position)
            if val > 4 and val < 10:
                cp_set.add(val)

        # update hashmap
        self.checkpoints_crossed[key] = cp_set
        return cp_set
        



