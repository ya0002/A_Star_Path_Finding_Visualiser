import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.config import Config
from kivy.graphics import Color
import A_Star

# setting the size of the window
Config.set('graphics','resizable',False)
Config.set('graphics','width',500)
Config.set('graphics','height',600)

class Interface(GridLayout):

    def __init__(self,**kwargs):
        super(Interface,self).__init__(**kwargs)
        self.rows = 2
        self.count=0
        self.corrected_row={0:9,1:8,2:7,3:6,4:5,5:4,6:3,7:2,8:1,9:0}
        self.source_r_GUI=None
        self.source_c_GUI=None
        self.target_r_GUI=None
        self.target_c_GUI=None

        with self.canvas:
            for j in range(10):
                for i in range(10):
                    Rectangle(pos=(i*50,j*50),size=(45,45))

    def on_touch_down(self, touch):
               # in kivy grid co-ordinates follow the format (col,row)
        print(self.corrected_row[touch.pos[1]//50],int(touch.pos[0]//50))   # it's basically corrected_row[COL//50] , int(ROW) => ROW , COL [normal]
        g_row=touch.pos[0]//50
        g_col=touch.pos[1]//50

        if self.count==0:
            self.set_source_GUI(g_row,g_col)
            self.count+=1

        elif self.count==1:
            self.set_target_GUI(g_row,g_col)
            self.count+=1

    def on_touch_move(self, touch):
        print(self.corrected_row[touch.pos[1]//50],int(touch.pos[0]//50))
        g_row=touch.pos[0]//50
        g_col=touch.pos[1]//50
        if self.count>1:
            self.set_obstacle_GUI(g_row,g_col)

    def set_source_GUI(self,g_row,g_col):
        with self.canvas:
            Color(1, 0, 0,.5,mode='rgba')
            Rectangle(pos=(g_row*50,g_col*50),size=(45,45))
            self.source_r_GUI=g_row
            self.source_c_GUI=g_col
            A_Star.source_r= self.corrected_row[g_col]
            A_Star.source_c=int(g_row)

    def set_target_GUI(self,g_row,g_col):
        with self.canvas:
            Color(0, 1, 0,.5,mode='rgba')
            Rectangle(pos=(g_row*50,g_col*50),size=(45,45))
            self.target_r_GUI=g_row
            self.target_c_GUI=g_col
            A_Star.target_r=self.corrected_row[g_col]
            A_Star.target_c=int(g_row)

    def set_obstacle_GUI(self,g_row,g_col):
        with self.canvas:
            if (g_row!=self.source_r_GUI or g_col!=self.source_c_GUI) and (g_row!=self.target_r_GUI or g_col!=self.target_c_GUI):
                Color(0, .5, .5,mode='rgb')
                Rectangle(pos=(g_row*50,g_col*50),size=(45,45))
                A_Star.obstacle_list.add((self.corrected_row[g_col],int(g_row)))
                A_Star.test_print()

class MyApp(App):
    def build(self):
        return Interface()


if __name__=="__main__":
    MyApp().run()