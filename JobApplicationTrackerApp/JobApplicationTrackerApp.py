import kivy
from UserData import UserData
from InfoDatabase import userInfoDatabase
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.graphics import Rectangle, Color
from kivy.uix.popup import Popup

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
        popup = Popup(title='Submission Successful!',content=Button(text='Application successfully stored. Click to close!'),size_hint=(None, None), size=(400, 400))
        popup.open()
        popup.content.bind(on_press=popup.dismiss)
        # Retrieve Data
        position = self.posInput.text
        company = self.companyInput.text
        DOS = self.SubmittedInput.text
        self.userData = UserData(position,company,DOS)
        db.insertDB(self.userData)
        # Clear text inputs
        self.posInput.text=''
        self.companyInput.text=''
        self.SubmittedInput.text=''
     
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
        self.viewFiledApps.bind(on_press=self.viewMyApps)
        self.add_widget(self.viewFiledApps)

    def go_fill_out_info(self,instance):
        jobApp.screen_manager.current = "userData"

    def viewMyApps(self,instance):
        jobApp.screen_manager.current = "viewApps"
        jobApp.viewApps.generateRows()
        

class ViewApplicationsPage(FloatLayout):
    # Create a page designated for the user to see all submissions made Bounds x[0 800] y [0 500
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ViewTitle = Label(text="Application Submission History",pos=(50,500),size=(750,100),size_hint=(None,None))
        self.jobLabel = Label(text="Job Position",pos=(0,400), size=(266,100),size_hint=(None,None))
        self.companyLabel = Label(text="Company",pos=(266,400), size=(266,100),size_hint=(None,None))
        self.submissionLabel = Label(text="Date of Submission",pos=(532,400), size=(266,100),size_hint=(None,None))
        self.returnButton = Button(text="Home Page", pos=(0,500),size=(200,100),size_hint=(None,None))
        self.returnButton.bind(on_press=self.viewToHome)
        self.CurrentPosition = (0,300)
        with self.returnButton.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.returnButton.pos,size = self.returnButton.size)
        with self.ViewTitle.canvas.before:
            Color(33/255,42/255,228/255,1)
            Rectangle(pos=self.ViewTitle.pos,size = self.ViewTitle.size)
        with self.jobLabel.canvas.before:
            Color(33/255,42/255,228/255,1)
            Rectangle(pos=self.jobLabel.pos,size = self.jobLabel.size)
        with self.companyLabel.canvas.before:
            Color(33/255,42/255,228/255,1)
            Rectangle(pos=self.companyLabel.pos,size = self.companyLabel.size)
        with self.submissionLabel.canvas.before:
            Color(33/255,42/255,228/255,1)
            Rectangle(pos=self.submissionLabel.pos,size = self.submissionLabel.size)
        self.add_widget(self.ViewTitle)
        self.add_widget(self.jobLabel)
        self.add_widget(self.companyLabel)
        self.add_widget(self.submissionLabel)
        self.add_widget(self.returnButton)

    def viewToHome(self,instance):
        jobApp.screen_manager.current = "start"

    def addRows(self,allData):
        position = allData[0]
        company = allData[1]
        submitted = allData[2]
        p_label = Label(text=str(position),pos=self.CurrentPosition, size=(266,100),size_hint=(None,None))
        c_label = Label(text=str(company),pos=(self.CurrentPosition[0]+266, self.CurrentPosition[1]), size=(266,100),size_hint=(None,None))
        s_label = Label(text=str(submitted),pos=(self.CurrentPosition[0]+532, self.CurrentPosition[1]), size=(266,100),size_hint=(None,None))
        with p_label.canvas.before:
            Color(33/255,42/255,228/255,1)
            Rectangle(pos=p_label.pos,size = p_label.size)
        with c_label.canvas.before:
            Color(33/255,42/255,228/255,1)
            Rectangle(pos=c_label.pos,size = c_label.size)
        with s_label.canvas.before:
            Color(33/255,42/255,228/255,1)
            Rectangle(pos=s_label.pos,size = s_label.size)
        self.CurrentPosition = (0,self.CurrentPosition[1]-100)
        self.add_widget(p_label)
        self.add_widget(c_label)
        self.add_widget(s_label)
        
    def generateRows(self):
        self.allData = db.getAllData()
        print(self.allData)
        for i in self.allData:
            self.addRows(i)
        self.allData = None
        


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
        # Add View Apps Page
        self.viewApps = ViewApplicationsPage()
        screen3 = Screen(name="viewApps")
        screen3.add_widget(self.viewApps)
        self.screen_manager.add_widget(screen3)
        return self.screen_manager

   
if __name__ == "__main__":
    jobApp = JobTrackerApp()
    db = userInfoDatabase()
    jobApp.run()
