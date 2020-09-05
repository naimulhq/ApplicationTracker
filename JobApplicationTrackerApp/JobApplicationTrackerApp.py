import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout


class HomePage(RelativeLayout):
    def __init__(self,**kwargs):
        super(RelativeLayout,self).__init__(**kwargs)
        # Add title for home screen
        title = Label(text="Job Application Tracker", font_size='50sp')
        title.color = [0,0,0,1]
        # Add title widget to RelativeLayout
        self.add_widget(title)
        

class JobTrackerApp(App):
    def build(self):
        # Set up the background color for the window
        r,g,b = 255,245,245
        Window.clearcolor = [float(r/255),float(g/255),float(b/255),1]
        # Set up home screen for app
        homeScreen = HomePage()
        return homeScreen
        
        
        

if __name__ == "__main__":
    JobTrackerApp().run()
