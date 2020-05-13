from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.config import Config
from kivy.graphics import Color
from kivy.clock import Clock
from functools import partial
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
        self.root_parent = None

    # function to calculate f_cost
    def calculate_fcost(self):
        self.f_cost = self.g_cost + self.h_cost


# Data structure to store nodes according to their F-cost or H-cost as needed
class PriorityQ:
    def __init__(self):
        self.Q = []
        self.Q_copy = []

    #  Q= [(node.f_cost,node),(),(), .....]
    def add(self, node, closed, thrown_out_of_closed):
        if node not in closed and node not in thrown_out_of_closed and node.obstacle == False:
            if len(self.Q) == 0:
                self.Q.append((node.f_cost, node))
            else:
                self.Qsort(node)
                if not node.target:
                    interface.trigger_useless(node)

    def Qsort(self, node):
        for i in range(len(self.Q)):

            # if F-costs are equal then the one with the lowest H-cost gets priority
            if self.Q[i][0] == node.f_cost:
                if self.Q[i][1].h_cost > node.h_cost:
                    self.Q.insert(i, (node.f_cost, node))
                    break

            # The lowest F-cost gets priority
            if self.Q[i][0] > node.f_cost:
                self.Q.insert(i, (node.f_cost, node))
                break

            # if the F-Cost to be added is the largest in the Q
            if i == len(self.Q) - 1:
                self.Q.append((node.f_cost, node))

    # Pop the first element, i.e. the one with the lowest F-cost
    def popQ(self):
        if len(self.Q) != 0:
            lowest = self.Q.pop(0)
            return lowest

    # append all the remaining elements of Q to Q_copy and then clear the Q.
    def copyQ(self):
        if len(self.Q) != 0:
            for i in self.Q:
                self.Q_copy.append(i)
            self.Q.clear()


# function to display grid
def show_grid():
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
def set_source(row, column):
    grid[row][column].source, grid[row][column].way = True, False


# function to set target node
def set_target(row, column):
    grid[row][column].target, grid[row][column].way = True, False


# function to set obstacle
def set_obstacle():
    for coordinate in obstacle_list:
        cell = grid[coordinate[0]][coordinate[1]]
        cell.obstacle, cell.way = True, False


# calculate h_cost for all nodes
def set_cost(currentrow, currentcol, target_r, target_c, parent, distance=1):
    dx = abs(target_r - currentrow)
    dy = abs(target_c - currentcol)
    # got this formula from Stanford's website on A* path finding(diagonal distance)
    grid[currentrow][currentcol].h_cost = (dx + dy) + ((1.4 - 2) * min(dx, dy))
    grid[currentrow][currentcol].g_cost = parent.g_cost + distance
    grid[currentrow][currentcol].calculate_fcost()


# function to add to open list/Q
def add_to_open(to_enter_row, to_enter_col, parent, open, closed, target_c, target_r, thrown_out_of_closed, distance=1):
    if to_enter_row >= 0 and to_enter_col >= 0:
        set_cost(to_enter_row, to_enter_col, target_r, target_c, parent, distance)
        open.add(grid[to_enter_row][to_enter_col], closed, thrown_out_of_closed)


def test_print():
    print('source-r', source_r, 'source_c', source_c)
    print('target-r', target_r, 'target_c', target_c)
    print(obstacle_list)
    print(len(obstacle_list))


def calculate():
    # Pinning source and target
    set_source(source_r, source_c)
    set_target(target_r, target_c)
    set_obstacle()

    source = grid[source_r][source_c]
    source.g_cost = 0

    open = PriorityQ()
    closed = []
    thrown_out_of_closed = []
    closed.append(source)
    parent = source
    dd = math.sqrt(2)  # diagonal distance , approx=1.4(root 2)
    break_counter = 0

    while True:

        # top left
        try:
            to_enter_row, to_enter_col = parent.row - 1, parent.col - 1
            add_to_open(to_enter_row, to_enter_col, parent, open, closed, target_c, target_r, thrown_out_of_closed, dd)
        except IndexError:
            pass

        # top
        try:
            to_enter_row, to_enter_col = parent.row - 1, parent.col
            add_to_open(to_enter_row, to_enter_col, parent, open, closed, target_c, target_r, thrown_out_of_closed)
        except IndexError:
            pass

        # top right
        try:
            to_enter_row, to_enter_col = parent.row - 1, parent.col + 1
            add_to_open(to_enter_row, to_enter_col, parent, open, closed, target_c, target_r, thrown_out_of_closed, dd)
        except IndexError:
            pass
        # ------------------------bottom-----------------------------------------
        # bottom left
        try:
            to_enter_row, to_enter_col = parent.row + 1, parent.col - 1
            add_to_open(to_enter_row, to_enter_col, parent, open, closed, target_c, target_r, thrown_out_of_closed, dd)
        except IndexError:
            pass

        # bottom
        try:
            to_enter_row, to_enter_col = parent.row + 1, parent.col
            add_to_open(to_enter_row, to_enter_col, parent, open, closed, target_c, target_r, thrown_out_of_closed)
        except IndexError:
            pass

        # bottom right
        try:
            to_enter_row, to_enter_col = parent.row + 1, parent.col + 1
            add_to_open(to_enter_row, to_enter_col, parent, open, closed, target_c, target_r, thrown_out_of_closed, dd)
        except IndexError:
            pass
        # ----------------------------------sides---------------------
        # left
        try:
            to_enter_row, to_enter_col = parent.row, parent.col - 1
            add_to_open(to_enter_row, to_enter_col, parent, open, closed, target_c, target_r, thrown_out_of_closed)
        except IndexError:
            pass

        # right
        try:
            to_enter_row, to_enter_col = parent.row, parent.col + 1
            add_to_open(to_enter_row, to_enter_col, parent, open, closed, target_c, target_r, thrown_out_of_closed)
        except IndexError:
            pass

        # if len(Q)==0 then no path exists
        if len(open.Q) == 0:
            if parent != source:
                parent.way, parent.path = True, False
                thrown_out_of_closed.append(parent)
                closed.remove(parent)
                parent = parent.root_parent
            else:
                break_counter += 1
        else:
            # gives the element with the lowest f_cost
            parent.way, parent.path = False, True
            if not parent.source:
                interface.trigger(parent)
            to_be_parent = open.popQ()[1]
            to_be_parent.root_parent = parent
            parent = to_be_parent
            closed.append(parent)

        if break_counter == 2:
            print('no valid path')
            break

        open.copyQ()

        # checking if the current node is the target node
        if parent.target:
            break

    source.path = False
    # display grid
    show_grid()


def reset():
    for i in grid:
        for j in i:
            if j.obstacle:
                j.obstacle, j.way = False, True
            elif j.source:
                j.source, j.way = False, True
            elif j.target:
                j.target, j.way = False, True
            elif j.path:
                j.path, j.way = False, True
    obstacle_list.clear()
#-------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------- GUI --------------------------------------------------

# setting the size of the window
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 500)
Config.set('graphics', 'height', 550)


class Interface(BoxLayout):
    size_factor = 8
    pos_factor = 10
    grid_size = 50

    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.wid = Widget()
        self.second = BoxLayout()

        self.start = Button(text='Start', size_hint=(.3, .17), pos_hint={'top': 1})
        self.start.bind(on_press=self.show_path)
        self.second.add_widget(self.start)

        self.reset = Button(text='reset', size_hint=(.3, .17), pos_hint={'top': 1})
        self.reset.bind(on_press=self.reset_grid)
        self.second.add_widget(self.reset)

        self.create_grid()

        self.count = 0
        self.corrected_row = {}
        for i in range(self.grid_size):
            self.corrected_row[i] = (self.grid_size - 1) - i

        self.source_r_GUI = None
        self.source_c_GUI = None
        self.target_r_GUI = None
        self.target_c_GUI = None

        self.timer = 0

        self.add_widget(self.second)
        self.add_widget(self.wid)

    def create_grid(self):
        with self.wid.canvas:
            for j in range(self.grid_size):
                Color(.9, .9, .9, 1, mode='rgba')
                for i in range(self.grid_size):
                    Rectangle(pos=(i * self.pos_factor, j * self.pos_factor), size=(self.size_factor, self.size_factor))

    def color_it(self, j, r, g, b, a, dt):
        print('IDHAR!')
        with self.wid.canvas:
            Color(r, g, b, a, mode='rgba')
            Rectangle(pos=(j.col * self.pos_factor, self.corrected_row[j.row] * self.pos_factor),
                      size=(self.size_factor, self.size_factor))

    def trigger(self, j):
        self.timer += 0.01
        Clock.schedule_once(partial(self.color_it, j, 1, 0, 0, 1), self.timer)

    def trigger_useless(self, j):
        Clock.schedule_once(partial(self.color_it, j, .3, .6, 1, .4), self.timer)

    def show_path(self, instance):
        print("button used")
        calculate()

    def reset_grid(self, instance):
        self.wid.canvas.clear()
        self.create_grid()
        self.count, self.timer = 0, 0
        reset()

    def on_touch_down(self, touch):
        super().on_touch_down(touch)

        try:
            # in kivy grid co-ordinates follow the format (col,row)
            print(self.corrected_row[touch.pos[1] // self.pos_factor], int(touch.pos[
                                                                               0] // self.pos_factor))  # it's basically corrected_row[COL//self.pos_factor] , int(ROW) => ROW , COL [normal]
            g_row = touch.pos[0] // self.pos_factor
            g_col = touch.pos[1] // self.pos_factor

            if self.count == 0:
                self.set_source_GUI(g_row, g_col)
                self.count += 1

            elif self.count == 1:
                self.set_target_GUI(g_row, g_col)
                self.count += 1
        except KeyError:
            pass

    def on_touch_move(self, touch):
        try:
            print(self.corrected_row[touch.pos[1] // self.pos_factor], int(touch.pos[0] // self.pos_factor))
            g_row = touch.pos[0] // self.pos_factor
            g_col = touch.pos[1] // self.pos_factor
            if self.count > 1:
                self.set_obstacle_GUI(g_row, g_col)
        except:
            pass

    def set_source_GUI(self, g_row, g_col):
        with self.wid.canvas:
            Color(1, 1, 0, 1, mode='rgba')
            Rectangle(pos=(g_row * self.pos_factor, g_col * self.pos_factor), size=(self.size_factor, self.size_factor))
            self.source_r_GUI = g_row
            self.source_c_GUI = g_col
            global source_r, source_c
            source_r = self.corrected_row[g_col]
            source_c = int(g_row)

    def set_target_GUI(self, g_row, g_col):
        with self.wid.canvas:
            Color(0, 1, 0, 1, mode='rgba')
            Rectangle(pos=(g_row * self.pos_factor, g_col * self.pos_factor), size=(self.size_factor, self.size_factor))
            self.target_r_GUI = g_row
            self.target_c_GUI = g_col
            global target_c, target_r
            target_r = self.corrected_row[g_col]
            target_c = int(g_row)

    def set_obstacle_GUI(self, g_row, g_col):
        with self.wid.canvas:
            if (g_row != self.source_r_GUI or g_col != self.source_c_GUI) and (
                    g_row != self.target_r_GUI or g_col != self.target_c_GUI):
                Color(0, .5, .5, mode='rgb')
                Rectangle(pos=(g_row * self.pos_factor, g_col * self.pos_factor),
                          size=(self.size_factor, self.size_factor))
                obstacle_list.add((self.corrected_row[g_col], int(g_row)))
                test_print()


interface = Interface()

class A_starApp(App):
    def build(self):
        return interface


# ----------------------------------------------------main------------------------------------------------------------------

# a grid of 50x50(49x49)
# (RESOLVED) 0th column shouldn't be used, if the input recieved from GUI contains col=0 add +1 to both cols.  PLOT EVRYTHING WITH col+1
grid = [[Node(i, j) for j in range(50)] for i in range(50)]
obstacle_list = set()

if __name__ == "__main__":
    A_starApp().run()
