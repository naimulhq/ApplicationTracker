import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class TrackerInfo(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        
        # Gather user info.

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
        self.add_widget(Label(text=""))

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
        
class JobTrackerApp(App):
    def build(self):
        return TrackerInfo()
         

if __name__ == "__main__":
    JobTrackerApp().run()
