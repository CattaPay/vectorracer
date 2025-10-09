
## a simplified version of vector racer that only concerns lattice points
SAFE = 0
HURT = 1

grid = [[HURT] * 7 + [SAFE] * 15 + [HURT] * 7,
        [HURT] * 6 + [SAFE] * 17 + [HURT] * 6,
        [HURT] * 5 + [SAFE] * 19 + [HURT] * 5,
        [HURT] * 4 + [SAFE] * 21 + [HURT] * 4,
        [HURT] * 4 + [SAFE] * 6 + [HURT] * 9 + [SAFE] * 6 + [HURT] * 4,
        [HURT] * 3 + [SAFE] * 6 + [HURT] * 11 + [SAFE] * 6 + [HURT] * 3,
        [HURT] * 3 + [SAFE] * 6 + [HURT] * 11 + [SAFE] * 6 + [HURT] * 3,
        [HURT] * 2 + [SAFE] * 6 + [HURT] * 13 + [SAFE] * 6 + [HURT] * 2,
        [HURT] * 2 + [SAFE] * 6 + [HURT] * 13 + [SAFE] * 6 + [HURT] * 2,
        [HURT] * 2 + [SAFE] * 6 + [HURT] * 13 + [SAFE] * 6 + [HURT] * 2,
        [HURT] * 2 + [SAFE] * 6 + [HURT] * 13 + [SAFE] * 6 + [HURT] * 2,
        [HURT] * 3 + [SAFE] * 6 + [HURT] * 11 + [SAFE] * 6 + [HURT] * 3,
        [HURT] * 3 + [SAFE] * 6 + [HURT] * 11 + [SAFE] * 6 + [HURT] * 3,
        [HURT] * 4 + [SAFE] * 6 + [HURT] * 9 + [SAFE] * 6 + [HURT] * 4,
        [HURT] * 4 + [SAFE] * 21 + [HURT] * 4,
        [HURT] * 5 + [SAFE] * 19 + [HURT] * 5,
        [HURT] * 6 + [SAFE] * 17 + [HURT] * 6,
        [HURT] * 7 + [SAFE] * 15 + [HURT] * 7]

HEIGHT = len(grid)
WIDTH = len(grid[0])

def printgrid(grid, current_square):
    for i in range(len(grid)):
        row = grid[i]
        for j in range(len(row)):
            val = grid[i][j]
            if i == current_square[0] and j == current_square[1]:
                print("S ", end = "")
            elif val == 0:
                print("  ", end = "")
            else:
                print("X ", end = "")
        print()

# check if it's on an X or out of bounds
# returns true if it's in the grid, false otherwise
def issafe(grid, current_square):
    height = len(grid)
    width = len(grid[0])
    i = current_square[0]
    j = current_square[1]
    if i < 0 or i >= height or j < 0 or j >= width:
        return False

    value = grid[i][j]
    if value == SAFE:
        return True
    else:
        return False


start_square = [15, 14]
velo = [0,0]
moves = []
for i in range(3):
    for j in range(3):
        moves.append((i-1,j-1))

current_square = start_square
while True:
    printgrid(grid, current_square)
    print()
    for i in range(len(moves)):
        print(i, moves[i])

    if not issafe(grid, current_square):
        print("Game Over")
        break

    choice = int(input("Choose your move: "))

    movechoice = moves[choice]

    # update velo
    velo[0] += movechoice[0]
    velo[1] += movechoice[1]

    # update score
    current_square[0] += velo[0]
    current_square[1] += velo[1]

    
    
