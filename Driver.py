
from track import Track

FINISHED = 2
OKAY = 1
BAD = -1

class Driver:
    # location
    # velocity
    # mode (orthogonal, corners allowed, 2 steps?)
    # current checkpoint
    # time since start of race
    #

    def __init__(self, track: Track, step_size = 15):
        self.track = track
        self.step_size = step_size
        self.velocity = [0,0]
        self.location = self.getStart()
        self.current_checkpoint = 0
        pass

    def copy(self):
        out = Driver(self.track, self.step_size)
        out.location[0] = self.location[0]
        out.location[1] = self.location[1]
        out.velocity[0] = self.velocity[0]
        out.velocity[1] = self.velocity[1]
        out.current_checkpoint = self.current_checkpoint
        return out


    def getStart(self):
        x,y = self.track.getStart()
        return [x,y]
    
    def checkEnd(self):
        return self.current_checkpoint == self.track.n_checkpoints
    
    def getGroundType(self):
        return self.track.getCell(self.location)
    
    def getActions(self):
        # if type is normal
        # need to add things if on gravel, curb or diff move type
        return [(1,1), (0,1), (-1,1),
                (1,0), (0,0), (-1,0),
                (1,-1), (0,-1), (-1,-1)]
    
    # gets all possible next states
    def getAdjacent(self):
        possible_actions = self.getActions()
        nextStates = []
        for action in possible_actions:
            newNode = self.copy()
            status = newNode.move(action)
            if status != BAD:
                nextStates.append(newNode)
        return nextStates

    
    # relies on step_size
    def endLocation(self):
        end = [self.location[0] + self.velocity[0] * self.step_size,
               self.location[1] + self.velocity[1] * self.step_size]
        return end
    
    def checkPath(self, end):
        return self.track.checkValid(self.location, end)
    
    def move(self, action):
        # update velocity
        self.velocity[0] += action[0]
        self.velocity[1] += action[1]

        # update position
        target_position = self.endLocation()

        # check if path is valid
        isValid = self.checkPath(target_position)
        if not isValid:
            # print("Hit a wall")
            # reset velocity
            self.velocity[0] -= action[0]
            self.velocity[1] -= action[1]
            return BAD
        
        # if path is valid, check if it crosses checkpoints
        checkpoints = self.track.checkCheckpoint(self.location, target_position)
        
        # if it crossed the next one, update... repeat if it crossed multiple
        for i in range(5):
            if self.current_checkpoint in checkpoints:
                self.current_checkpoint += 1
            else:
                break
        
        # if path is valid, move to new point, increment time
        self.location = target_position
        self.time += 1
        
        # if finished, 
        if self.checkEnd():
            return FINISHED

        # success
        return OKAY
    
    def safeMove(self, action):
        out = self.move(action)
        if out == None:
            print("Hit a wall")
            return self
        
        if self.check_end():
            print("Done!")
            return self
        
        return self
    
    def getHeuristic(self):
        return self.track.getHeuristic(self.location, self.velocity, self.current_checkpoint)








    
    
        
    


        
