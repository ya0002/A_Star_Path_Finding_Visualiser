class Node:
    def __init__(self):
        self.g_cost, self.h_cost = 0, 0
        self.f_cost = self.g_cost + self.h_cost
        self.path = True
        self.obstacle = False
        self.source = False
        self.target = False


# function to display grid
def show_grid(grid):
    for i in grid:
        for j in i:
            if j.path:
                print("-", end=" ")
            elif j.obstacle:
                print("O", end=" ")
            elif j.source:
                print("S", end=" ")
            elif j.target:
                print("T", end=" ")
        print()


# function to set source node
def set_source(grid, row, column):
    grid[row][column].source, grid[row][column].path = True, False


# function to set target node
def set_target(grid, row, column):
    grid[row][column].target, grid[row][column].path = True, False


# calculate g_cost and h_cost
def set_cost(grid):
    pass



# -----------------------------------------------------------------------------------------

# a grid of 5x10(4x9)
grid = [[Node() for _ in range(10)] for i in range(5)]

set_source(grid, 0, 0)
set_target(grid, 4, 9)

show_grid(grid)
