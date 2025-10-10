

## 

from track import Track
from driver import Driver
from node import Node
import heapq


REMOVED = "removed"
# list of drivers... interfaces with
class DriverList:
    def __init__(self, nodeMap):
        self.values = []
        self.nodeMap = nodeMap
        self.entry_finder = {} # jank chatgpt solution to removing elems
        self.counter = 0 # breaks ties
    
    # changes an elements priority
    # or adds it if it's not in queue
    def push(self, driver: Driver):
        # if task already in queue, mark old one as removed
        node : Node = self.nodeMap[driver]
        if driver in self.entry_finder:
            self.entry_finder[driver][-1] = REMOVED

        entry = [node.getValue(), self.counter, driver]
        self.entry_finder[driver] = entry
        heapq.heappush(self.values, entry)
        self.counter += 1

    def pop(self) -> Driver:
        while self.values:
            priority, priority2, item = heapq.heappop(self.values)
            if item != REMOVED:
                del self.entry_finder[item]
                return item
        print("pop from empty queue")
        return None
    
    def size(self):
        return len(self.values)
    
    def empty(self):
        return self.size() == 0

## hashset of positions seen before
# maps positions to the node representing them
positions_seen = {}

# fancy priority queue
frontier = DriverList(positions_seen)

print("Initializing Track")
track = Track("images/clean_maze2.png")
#track = Track("images/test_track.png")

# for simplicity lol
# track.n_checkpoints = 5

start_pos = Driver(track)
start_node = Node(start_pos, time = 0, prev = None, heuristic = start_pos.getHeuristic())
positions_seen[start_pos] = start_node

# push start_pos onto heap
frontier.push(start_pos)

print("Searching")
counter = 0

## max time
max_time = 1000

# list of solutions
solutions = []

while not frontier.empty():
    # pop first driver off of frontier
    driver = frontier.pop()
    prevNode : Node = positions_seen[driver]

    counter += 1
    if counter % 100 == 0:
        print(driver.current_checkpoint,prevNode.driver.location, prevNode.driver.velocity, prevNode.best_time, prevNode.heuristic)

    if prevNode.getTime() <= max_time:
        # check if finished
        if driver.checkEnd():
            solutions.append(prevNode)
            max_time = prevNode.getTime()
        else:
            adjacents = driver.getAdjacent()
            for newDriver in adjacents:
                # if seen before, check if it's better than previous
                    
                if newDriver in positions_seen:
                    oldNode:Node = positions_seen[newDriver]

                    # if oldNode's time is worse than newDriver's replace it and its path
                    if oldNode.getTime() > prevNode.getTime() + 1:
                        oldNode.updateTime(prevNode.getTime() + 1)
                        oldNode.updatePrev(prevNode)

                        # then add/update frontier
                        frontier.push(newDriver)
            
                # if not seen before, add node to positions seen and add driver to frontier
                else:
                    # create new node object
                    newNode = Node(newDriver, prevNode.getTime() + 1, prevNode, newDriver.getHeuristic())

                    # add driver -> node to positions seen
                    positions_seen[newDriver] = newNode

                    # add driver to frontier
                    frontier.push(newDriver)

# def printVelocitiesRecursive(node: Node):
#     print(node.driver.velocity, node.driver.location, node.driver.current_checkpoint)
#     if node.prev != None:
#         printVelocitiesRecursive(node.prev)

def getVelocitiesRecursive(node: Node, box : list):
    box.append((node.driver.velocity, node.driver.location, node.driver.current_checkpoint))
    if node.prev != None:
        getVelocitiesRecursive(node.prev, box)


def printVelocitiesRecursive(node: Node):
    print(node.driver.velocity, node.driver.location, node.driver.current_checkpoint)
    if node.prev != None:
        printVelocitiesRecursive(node.prev)

import numpy as np

def distAlongLine(start_pos, end_pos, point):
    A = np.array(start_pos)
    B = np.array(end_pos)
    P = np.array(point)

    AB = B - A
    AP = P - A
    return np.dot(AP, AB) / np.dot(AB, AB)

def distFromLine(start_pos, end_pos, point):
    num = ((end_pos[0] - start_pos[0]) * (start_pos[1] - point[1]) - (end_pos[1] - start_pos[1]) * (start_pos[0] - point[0])) ** 2
    denom = (end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2
    return num / denom


def getFinalTime(node:Node, tol = 1):
    prevNode = node.prev
    end_location = node.driver.location
    start_location = prevNode.driver.location

    finish = node.driver.track.checkpoints[-1]

    vals = []
    for point in finish:
        if distFromLine(start_location, end_location, point) <= tol ** 2:
            vals.append(distAlongLine(start_location, end_location, point))
    
    if len(vals) == 0:
        print("hmm")
        return 100
    
    return min(vals)


best_node = None
best_score = 3

for node in solutions:
    score = getFinalTime(node)
    print(score)
    if score < best_score:
        best_score = score
        best_node = node
        
def printAccelerations(node: Node):
    box = []
    getVelocitiesRecursive(node, box)

    for i in range(len(box)-1):
        print(box[i][0][0] - box[i+1][0][0], box[i][0][1] - box[i+1][0][1])
        
print()
printVelocitiesRecursive(best_node)


print(best_score)
print(best_node.getTime())
print(len(solutions))
printAccelerations(best_node)
