

## 

from track import Track
from driver import Driver
import queue

track = Track("example_mask.png")
start_pos = Driver(track)


## hashset of positions seen before
# map of the best time to each position

positions_seen = {}


# list of frontier positions to investigate
# can be replaced with some sort of queue later maybe
current_positions = queue.Queue()
current_positions.put(start_pos)

while not current_positions.empty():
    node = current_positions.get()

    # check if finished
    # if finished with best time, save to bests
