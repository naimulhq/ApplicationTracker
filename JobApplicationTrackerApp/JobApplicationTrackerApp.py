import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.screenmanager import FadeTransition

class TrackerInfo(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        # Gather the position that is being applied for
        self.add_widget(Label(text="Job Position"))
        self.posInput = TextInput(multiline = False)
        self.add_widget(self.posInput)

        # Gather info regarding the company that is being applied to
        self.add_widget(Label(text="Company"))
        self.companyInput = TextInput(multiline = False)
        self.add_widget(self.companyInput)

        # User enters data when application was applied for
        self.add_widget(Label(text="Date of Submission"))
        self.SubmittedInput = TextInput(multiline = False)
        self.add_widget(self.SubmittedInput)

        # Added a blank label for asthetic purposes
        self.backButton = Button(text="Return to Home Page",font_size=14)
        self.backButton.bind(on_press=self.go_home)
        self.add_widget(self.backButton)

        # Create a submit button
        self.submitButton = Button(text="Submit", font_size=14)
        r,g,b= 33,42,228
        self.submitButton.background_color = [float(r)/255,float(g)/255,float(b)/255,1]
        self.submitButton.bind(on_press=self.submit_info) # When button is pressed, will go to method submitInfo
        self.add_widget(self.submitButton)

    def submit_info(self,instance):
        # Get all of the values from input
        position = self.posInput.text
        company = self.companyInput.text
        DOS = self.SubmittedInput.text
        print("Job Application Info")
        print(position,company,DOS)

    def go_home(self,instance):
        print("Going to Home Page")
        jobApp.screen_manager.current = "start"



class StartUpPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Job Tracker Application",font_size='20sp',valign="top",halign="center"))
        self.infoButton = Button(text="Enter Newly Filed Job Application")
        self.infoButton.bind(on_press=self.go_fill_out_info)
        self.add_widget(self.infoButton)
        self.viewFiledApps = Button(text="View Filed Application")
        self.add_widget(self.viewFiledApps)

    def go_fill_out_info(self,instance):
        jobApp.screen_manager.current = "userData"
        
class JobTrackerApp(App):
    def build(self):
        # Screen Manager manages all the screens in the application
        self.screen_manager = ScreenManager()
        # Add Starting Page
        self.startPage = StartUpPage()
        screen1 = Screen(name="start")
        screen1.add_widget(self.startPage)
        self.screen_manager.add_widget(screen1)
        # Add Info Page to Screen
        self.addInfoPage = TrackerInfo()
        screen2 = Screen(name="userData")
        screen2.add_widget(self.addInfoPage)
        self.screen_manager.add_widget(screen2)
        return self.screen_manager

        
         

if __name__ == "__main__":
    jobApp = JobTrackerApp()
    jobApp.run()
