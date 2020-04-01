from queue import PriorityQueue as PQ


class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.g_cost, self.h_cost = 0, 0
        self.f_cost = 0
        self.way = True
        self.obstacle = False
        self.source = False
        self.target = False
        self.path = False

    # function to calculate f_cost
    def calculate_fcost(self):
        self.f_cost = self.g_cost + self.h_cost

    # Overloading '<'(less than) operator
    def __lt__(self, other):
        return self.f_cost < other.f_cost


# function to display grid
def show_grid(grid):
    for i in grid:
        for j in i:
            if j.way:
                print("-", end=" ")
            elif j.obstacle:
                print("O", end=" ")
            elif j.source:
                print("S", end=" ")
            elif j.target:
                print("T", end=" ")
            elif j.path:
                print("x", end=" ")
        print()


# function to set source node
def set_source(grid, row, column):
    grid[row][column].source, grid[row][column].way = True, False


# function to set target node
def set_target(grid, row, column):
    grid[row][column].target, grid[row][column].way = True, False


# calculate g_cost and h_cost
def set_cost(grid, source_r, source_c, target_r, target_c):
    for currentrow in range(len(grid)):
        for currentcol in range(currentrow):
            grid[currentrow][currentcol].g_cost = (abs(source_r - currentrow) + abs(source_c - currentcol))**1/2
            grid[currentrow][currentcol].h_cost = (abs(target_r - currentrow) + abs(target_c - currentcol))**1/2
            grid[currentrow][currentcol].calculate_fcost()


def enter(grid,open,closed,to_enter_row,to_enter_col):
    if to_enter_row>=0 and to_enter_col>=0:
        to_enter = grid[to_enter_row][to_enter_col]
        if to_enter not in closed:
            open.put((to_enter.f_cost, to_enter))


# ----------------------------------------------------------------------------------------------------------------------

# a grid of 5x10(4x9)
grid = [[Node(i, j) for j in range(10)] for i in range(5)]

# enter the coordinates of source and target
source_r, source_c = map(int, input("Enter coordinates of source: ").split(","))
target_r, target_c = map(int, input("Enter coordinates of target: ").split(","))

# Pinning source and target
set_source(grid, source_r, source_c)
set_target(grid, target_r, target_c)
set_cost(grid, source_r, source_c, target_r, target_c)

source = grid[source_r][source_c]
# target = grid[target_r][target_c]
open = PQ()
closed = []
closed.append(source)
current = source

while True:

    # top left
    try:
        to_enter_row,to_enter_col=current.row-1,current.col - 1
        enter(grid,open,closed,to_enter_row,to_enter_col)
    except IndexError:
        continue

    # top
    try:
        to_enter_row,to_enter_col = current.row - 1,current.col
        enter(grid,open,closed,to_enter_row,to_enter_col)
    except IndexError:
        continue

    # top right
    try:
        to_enter_row,to_enter_col = current.row - 1,current.col + 1
        enter(grid,open,closed,to_enter_row,to_enter_col)
    except IndexError:
        continue
    # ------------------------bottom-----------------------------------------
    # bottom left
    try:
        to_enter_row,to_enter_col = current.row + 1,current.col - 1
        enter(grid,open,closed,to_enter_row,to_enter_col)
    except IndexError:
        continue

    # bottom
    try:
        to_enter_row,to_enter_col = current.row + 1,current.col
        enter(grid,open,closed,to_enter_row,to_enter_col)
    except IndexError:
        continue

    # bottom right
    try:
        to_enter_row,to_enter_col = current.row + 1,current.col + 1
        enter(grid,open,closed,to_enter_row,to_enter_col)
    except IndexError:
        continue
    # ----------------------------------sides---------------------
    # left
    try:
        to_enter_row,to_enter_col = current.row,current.col - 1
        enter(grid,open,closed,to_enter_row,to_enter_col)
    except IndexError:
        continue

    # right
    try:
        to_enter_row,to_enter_col = current.row,current.col + 1
        enter(grid,open,closed,to_enter_row,to_enter_col)
    except IndexError:
        continue

    current = open.get()[1]
    current.path, current.way = True, False
    closed.append(current)

    while not open.empty():
        open.get()

    if current.target:
        break

show_grid(grid)
