import heapdict as HD
import copy


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


# calculate g_cost and h_cost for all nodes
def set_cost(grid, source_r, source_c, target_r, target_c):
    for currentrow in range(len(grid)):
        for currentcol in range(currentrow):
            grid[currentrow][currentcol].h_cost = ((target_r - currentrow) ** 2 + (target_c - currentcol) ** 2) ** 1 / 2
            # grid[currentrow][currentcol].g_cost = ((source_r - currentrow) ** 2 + (source_c - currentcol) ** 2) ** 1 / 2
            grid[currentrow][currentcol].calculate_fcost()


# update g_cost and calculate f_cost
def update_cost(current, g_value, to_enter):
    dummy_g = current.g_cost + g_value
    if dummy_g < to_enter.g_cost or to_enter.g_cost == 0:
        to_enter.g_cost = dummy_g
    to_enter.calculate_fcost()


# function to add/append a value to open
def enter(grid, open, closed, to_enter_row, to_enter_col, current, g_value=1):
    if to_enter_row >= 0 and to_enter_col >= 0:
        to_enter = grid[to_enter_row][to_enter_col]
        # to avoid copying the address
        dummy_to_enter = copy.deepcopy(to_enter)
        # updating g_cost if required
        update_cost(current, g_value, dummy_to_enter)
        # checking value to be added to open isn't in closed
        if to_enter not in closed:
            g_list = list(open.values())
            for i in g_list:
                if i.row == dummy_to_enter.row and i.col == dummy_to_enter.col:
                    # selecting the one with lowest g_cost
                    if i.g_cost > dummy_to_enter.g_cost:
                        to_enter = copy.deepcopy(dummy_to_enter)
                    open[to_enter.f_cost] = to_enter
                    return 0  # just to end the function
            open[to_enter.f_cost] = to_enter


# ----------------------------------------------------main------------------------------------------------------------------
if __name__ == '__main__':
    # a grid of 5x10(4x9)
    grid = [[Node(i, j) for j in range(10)] for i in range(5)]

    # enter the coordinates of source and target
    source_r, source_c = map(int, input("Enter coordinates of source: ").split(","))
    target_r, target_c = map(int, input("Enter coordinates of target: ").split(","))

    # Pinning source and target
    set_source(grid, source_r, source_c)
    set_target(grid, target_r, target_c)

    # setting g_cost and h_cost for every node
    set_cost(grid, source_r, source_c, target_r, target_c)

    source = grid[source_r][source_c]

    open = HD.heapdict()
    closed = []
    closed.append(source)
    current = source

    while True:

        # top left
        try:
            to_enter_row, to_enter_col = current.row - 1, current.col - 1
            enter(grid, open, closed, to_enter_row, to_enter_col, current, 1.4)
        except IndexError:
            continue

        # top
        try:
            to_enter_row, to_enter_col = current.row - 1, current.col
            enter(grid, open, closed, to_enter_row, to_enter_col, current)
        except IndexError:
            continue

        # top right
        try:
            to_enter_row, to_enter_col = current.row - 1, current.col + 1
            enter(grid, open, closed, to_enter_row, to_enter_col, current, 1.4)
        except IndexError:
            continue
        # ------------------------bottom-----------------------------------------
        # bottom left
        try:
            to_enter_row, to_enter_col = current.row + 1, current.col - 1
            enter(grid, open, closed, to_enter_row, to_enter_col, current, 1.4)
        except IndexError:
            continue

        # bottom
        try:
            to_enter_row, to_enter_col = current.row + 1, current.col
            enter(grid, open, closed, to_enter_row, to_enter_col, current)
        except IndexError:
            continue

        # bottom right
        try:
            to_enter_row, to_enter_col = current.row + 1, current.col + 1
            enter(grid, open, closed, to_enter_row, to_enter_col, current, 1.4)
        except IndexError:
            continue
        # ----------------------------------sides---------------------
        # left
        try:
            to_enter_row, to_enter_col = current.row, current.col - 1
            enter(grid, open, closed, to_enter_row, to_enter_col, current)
        except IndexError:
            continue

        # right
        try:
            to_enter_row, to_enter_col = current.row, current.col + 1
            enter(grid, open, closed, to_enter_row, to_enter_col, current)
        except IndexError:
            continue

        # gives the element with the lowest f_cost
        current = open.popitem()[1]
        current.path, current.way = True, False
        closed.append(current)

        # checking if the current node is the target node
        if current.target:
            break

    # display grid
    show_grid(grid)
