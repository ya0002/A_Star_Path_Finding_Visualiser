import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.config import Config

Config.set('graphics','resizable',False)
Config.set('graphics','width',500)
Config.set('graphics','height',600)

class Interface(GridLayout):

    def __init__(self,**kwargs):
        super(Interface,self).__init__(**kwargs)
        self.cols= 2
        self.rows = 5

        with self.canvas:
            for j in range(10):
                for i in range(10):
                    Rectangle(pos=(i*50,j*50),size=(45,45))

class MyApp(App):
    def build(self):
        return Interface()


MyApp().run()