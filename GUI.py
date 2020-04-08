import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.config import Config
from kivy.graphics import Color

# setting the size of the window
Config.set('graphics','resizable',False)
Config.set('graphics','width',500)
Config.set('graphics','height',600)

class Interface(GridLayout):

    def __init__(self,**kwargs):
        super(Interface,self).__init__(**kwargs)
        # self.cols= 1
        self.rows = 2
        self.count=0
        with self.canvas:
            for j in range(10):
                for i in range(10):
                    Rectangle(pos=(i*50,j*50),size=(45,45))

    def on_touch_down(self, touch):
        corrected_row={0:9,1:8,2:7,3:6,4:5,5:4,6:3,7:2,8:1,9:0}        # in kivy grids are in the form (col,row)
        print(corrected_row[touch.pos[1]//50],int(touch.pos[0]//50))   # it's basically corrected_row[col//50] , int(row)
        g_row=touch.pos[0]//50
        g_col=touch.pos[1]//50

        if self.count==0:
            self.set_source_GUI(g_row,g_col)
            self.count+=1

        elif self.count==1:
            self.set_target_GUI(g_row,g_col)
            self.count+=1

    def set_source_GUI(self,g_row,g_col):
        with self.canvas:
            Color(1, 0, 0,mode='rgb')
            Rectangle(pos=(g_row*50,g_col*50),size=(45,45))

    def set_target_GUI(self,g_row,g_col):
        with self.canvas:
            Color(0, 1, 0,mode='rgb')
            Rectangle(pos=(g_row*50,g_col*50),size=(45,45))

class MyApp(App):
    def build(self):
        return Interface()


MyApp().run()