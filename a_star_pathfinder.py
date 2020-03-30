class Node:
    def __init__(self, g_cost=0, h_cost=0,path=0,obstacle=0,source=0,target=0):
        self.f_cost = g_cost + h_cost
        self.path=path
        self.obstacle=obstacle
        self.source=source
        self.target=target

# function to display grid
def show_grid(grid):
    for i in grid:
        for j in i:
            if j.path==1:
                print("-",end=" ")
            elif j.obstacle==1:
                print("O",end=" ")
            elif j.source==1:
                print("S", end=" ")
            elif j.target==1:
                print("T",end=" ")
        print()

#function to set source node
def set_source(grid,row,column):
    grid[row][column].source,grid[row][column].path=1,0

#function to set target node
def set_target(grid,row,column):
    grid[row][column].target,grid[row][column].path=1,0


#-----------------------------------------------------------------------------------------

#a grid of 5x10(4x9)
grid=[[Node(0,0,1) for _ in range(10)] for i in range(5)]

set_source(grid,0,0)
set_target(grid,4,9)

show_grid(grid)