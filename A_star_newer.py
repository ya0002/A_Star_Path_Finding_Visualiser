import math
# to store each node of the graph
class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.g_cost, self.h_cost = None, 0
        self.f_cost = 0
        self.way = True
        self.obstacle = False
        self.source = False
        self.target = False
        self.path = False
        self.parent = None

    # function to calculate f_cost
    def calculate_fcost(self):
        self.f_cost = self.g_cost + self.h_cost

#Data structure to store nodes according to their F-cost or H-cost as needed
class PriorityQ:
    def __init__(self):
        self.Q = []
        self.Q_copy=[]

    #  Q= [(node.f_cost,node),(),(), .....]
    def add(self, node, closed):
        if node not in closed and node.obstacle==False:
            if len(self.Q) == 0:
                self.Q.append((node.f_cost, node))
            else:
                self.Qsort(node)

    def Qsort(self, node):
        for i in range(len(self.Q)):

            if self.Q[i][0] == node.f_cost:
                if self.Q[i][1].h_cost > node.h_cost:
                    self.Q.insert(i, (node.f_cost, node))
                    break

            if self.Q[i][0] > node.f_cost:
                self.Q.insert(i, (node.f_cost, node))
                break

            if i == len(self.Q) - 1:
                self.Q.append((node.f_cost, node))

    def popQ(self):
        if len(self.Q)!=0:
            lowest=self.Q.pop(0)
            return lowest

    def copyQ(self):
        if len(self.Q)!=0:
            for i in self.Q:
                self.Q_copy.append(i)
            self.Q.clear()

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

#function to set obstacle
def set_obstacle(grid, row, column):
    grid[row][column].obstacle, grid[row][column].way = True, False


# calculate h_cost for all nodes
def set_cost(grid, currentrow, currentcol, target_r, target_c, parent, distance=1):
    dx = abs(target_r - currentrow)
    dy = abs(target_c - currentcol)
    grid[currentrow][currentcol].h_cost = (dx + dy) + ((1.4 - 2) * min(dx, dy))
    dummy_g=parent.g_cost + distance
    # if grid[currentrow][currentcol].g_cost==None or dummy_g<grid[currentrow][currentcol].g_cost :
    #     grid[currentrow][currentcol].g_cost =dummy_g
    grid[currentrow][currentcol].g_cost =dummy_g
    grid[currentrow][currentcol].calculate_fcost()

def add_to_open(grid,to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,distance=1 ):
    if to_enter_row>=0 and to_enter_col>0:
        set_cost(grid, to_enter_row, to_enter_col, target_r, target_c, parent,distance)
        open.add(grid[to_enter_row][to_enter_col],closed)

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
    # set_obstacle(grid, 0, 1)
    # set_obstacle(grid, 0, 2)
    # set_obstacle(grid, 3, 8)
    source = grid[source_r][source_c]
    source.g_cost = 0

    open = PriorityQ()
    closed = []
    closed.append(source)
    parent = source
    dd=math.sqrt(2)
    while True:

        # top left
        try:
            to_enter_row, to_enter_col = parent.row - 1, parent.col - 1
            add_to_open(grid,to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,dd )
        except IndexError:
            pass

        # top
        try:
            to_enter_row, to_enter_col = parent.row - 1, parent.col
            add_to_open(grid,to_enter_row,to_enter_col,parent,open,closed,target_c,target_r)
        except IndexError:
            pass

        # top right
        try:
            to_enter_row, to_enter_col = parent.row - 1, parent.col + 1
            add_to_open(grid,to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,dd )
        except IndexError:
            pass
        # ------------------------bottom-----------------------------------------
        # bottom left
        try:
            to_enter_row, to_enter_col = parent.row + 1, parent.col - 1
            add_to_open(grid,to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,dd )
        except IndexError:
            pass

        # bottom
        try:
            to_enter_row, to_enter_col = parent.row + 1, parent.col
            add_to_open(grid,to_enter_row,to_enter_col,parent,open,closed,target_c,target_r)
        except IndexError:
            pass

        # bottom right
        try:
            to_enter_row, to_enter_col = parent.row + 1, parent.col + 1
            add_to_open(grid,to_enter_row,to_enter_col,parent,open,closed,target_c,target_r,dd )
        except IndexError:
            pass
        # ----------------------------------sides---------------------
        # left
        try:
            to_enter_row, to_enter_col = parent.row, parent.col - 1
            add_to_open(grid,to_enter_row,to_enter_col,parent,open,closed,target_c,target_r)
        except IndexError:
            pass

        # right
        try:
            to_enter_row, to_enter_col = parent.row, parent.col + 1
            add_to_open(grid,to_enter_row,to_enter_col,parent,open,closed,target_c,target_r)
        except IndexError:
            pass

        # gives the element with the lowest f_cost
        parent.way,parent.path=False,True
        to_be_parent=open.popQ()[1]
        to_be_parent.parent=parent
        parent=to_be_parent
        closed.append(parent)

        open.copyQ()

        # checking if the current node is the target node
        if parent.target:
            break

    # display grid
    show_grid(grid)
