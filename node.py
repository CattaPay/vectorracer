
from driver import Driver
## a node consists of a driver, best time, heuristic value, and previous node

class Node:
    def __init__(self, driver: Driver, time, prev = None, heuristic = None):
        self.driver = driver
        self.best_time = time
        self.prev = prev
        self.heuristic = heuristic

    def getTime(self):
        return self.best_time

    def updateTime(self, newTime):
        self.best_time = newTime

    def getPrev(self):
        return self.prev
    
    def updatePrev(self, newPrev):
        self.prev = newPrev

    def adjacentDrivers(self):
        return self.driver.getAdjacent()
    



