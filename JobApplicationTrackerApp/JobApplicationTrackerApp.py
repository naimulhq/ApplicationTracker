import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


class jobTrackerTable(BoxLayout):
    def __init__(self, **kwargs):
        super(jobTrackerTable,self).__init__(**kwargs)
        self.orientation = "vertical"
        
       

class JobTrackerApp(App):
    def build(self):
        return jobTrackerTable()

if __name__ == "__main__":
    JobTrackerApp().run()
