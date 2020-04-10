from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.config import Config
from kivy.graphics import Color
import A_Star

# setting the size of the window
Config.set('graphics','resizable',False)
Config.set('graphics','width',500)
Config.set('graphics','height',600)

class Interface(BoxLayout):

    def __init__(self,**kwargs):
        super(Interface,self).__init__(**kwargs)

        self.orientation='vertical'

        self.wid=Widget()
        self.second=BoxLayout()

        self.start=Button(text='Start',size_hint=(.3,.17),pos_hint={'top':1})
        self.start.bind(on_press=self.show_path)
        self.second.add_widget(self.start)

        self.create_grid()

        self.count=0
        self.corrected_row={0:9,1:8,2:7,3:6,4:5,5:4,6:3,7:2,8:1,9:0}
        self.source_r_GUI=None
        self.source_c_GUI=None
        self.target_r_GUI=None
        self.target_c_GUI=None

        self.add_widget(self.second)
        self.add_widget(self.wid)



    def create_grid(self):
        with self.wid.canvas:
            for j in range(10):
                for i in range(10):
                    Rectangle(pos=(i*50,j*50),size=(45,45))

    def show_path(self, instance):
        print("button used")
        A_Star.calculate()
        grid=A_Star.grid
        for i in grid:
            for j in i:
                if j.path:
                    print('path maker ',j.row, j.col)
                    with self.wid.canvas:
                        Color(1, 1, 0,.4,mode='rgba')
                        Rectangle(pos=(j.col*50,self.corrected_row[j.row]*50),size=(45,45))


    def on_touch_down(self, touch):
        super().on_touch_down(touch)

        try:
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
        except KeyError:
            pass

    def on_touch_move(self, touch):
        try:
            print(self.corrected_row[touch.pos[1]//50],int(touch.pos[0]//50))
            g_row=touch.pos[0]//50
            g_col=touch.pos[1]//50
            if self.count>1:
                self.set_obstacle_GUI(g_row,g_col)
        except:
            pass

    def set_source_GUI(self,g_row,g_col):
        with self.wid.canvas:
            Color(1, 0, 0,.5,mode='rgba')
            Rectangle(pos=(g_row*50,g_col*50),size=(45,45))
            self.source_r_GUI=g_row
            self.source_c_GUI=g_col
            A_Star.source_r= self.corrected_row[g_col]
            A_Star.source_c=int(g_row)

    def set_target_GUI(self,g_row,g_col):
        with self.wid.canvas:
            Color(0, 1, 0,.5,mode='rgba')
            Rectangle(pos=(g_row*50,g_col*50),size=(45,45))
            self.target_r_GUI=g_row
            self.target_c_GUI=g_col
            A_Star.target_r=self.corrected_row[g_col]
            A_Star.target_c=int(g_row)

    def set_obstacle_GUI(self,g_row,g_col):
        with self.wid.canvas:
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
