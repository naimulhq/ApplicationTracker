import kivy
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from UserData import UserData, PotentialApps
from InfoDatabase import userInfoDatabase, potentialAppsDatabase
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
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.lang import Builder

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
        jobApp.screen_manager.current = "start"


# Start up page
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
        self.viewPotentialApps = Button(text="View Potentials Job Applications")
        self.viewPotentialApps.bind(on_press=self.go_potential_apps)
        self.add_widget(self.viewPotentialApps)
        self.enterPotentialApps = Button(text="Enter Potentials Job Applications")
        self.enterPotentialApps.bind(on_press=self.enter_potential_apps)
        self.add_widget(self.enterPotentialApps)

    def enter_potential_apps(self,instance):
        jobApp.screen_manager.current= "enterApps"

    def go_fill_out_info(self,instance):
        jobApp.screen_manager.current = "userData"

    def viewMyApps(self,instance):
        jobApp.screen_manager.current = "viewApps"
        jobApp.viewApps.generateRows()

    def go_potential_apps(self,instance):
        jobApp.screen_manager.current = "potentialApps"
        jobApp.potentialApps.generateRows()
        
        

class ViewApplicationsPage(FloatLayout):
    # Create a page designated for the user to see all submissions made Bounds x[0 800] y [0 500
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.generatePage()

    def viewToHome(self,instance):
        jobApp.screen_manager.current = "start"

    # Produces a popup indicating whether all values should be deleted. Call deleteAllEntries depending on result
    def clearAllEntries(self,instance):
        # Create a popup with two buttons
        self.popup = Popup(title="Are you sure? Clearing all entries can not be undone.",size_hint=(None,None), size=(400,400))
        box = BoxLayout()
        yesButton = Button(text="Yes")
        noButton = Button(text = "No")
        # Bind the button to two options
        noButton.bind(on_press=self.popup.dismiss)
        yesButton.bind(on_press=self.deleteAllEntries)
        # Add buttons to popup widget
        box.add_widget(yesButton)
        box.add_widget(noButton)
        self.popup.content = box
        self.popup.open()

    # In charge of deleting all entires
    def deleteAllEntries(self,instance):
        db.deleteAllData()
        self.popup.dismiss()
        self.clear_widgets()
        self.generatePage()

    # Performs the task of adding the actual row onto the FloatLayout
    def addRows(self,allData):
        # Create labels that will hold the actual values from database
        p_label = Label(text=str(allData[0]),pos=self.CurrentPosition, size=(266,100),size_hint=(None,None))
        c_label = Label(text=str(allData[1]),pos=(self.CurrentPosition[0]+266, self.CurrentPosition[1]), size=(266,100),size_hint=(None,None))
        s_label = Label(text=str(allData[2]),pos=(self.CurrentPosition[0]+532, self.CurrentPosition[1]), size=(266,100),size_hint=(None,None))
        # Create Recntangle and Change Color for each row
        with p_label.canvas.before:
            Color(33/255,42/255,228/255,1)
            Rectangle(pos=p_label.pos,size = p_label.size)
        with c_label.canvas.before:
            Color(33/255,42/255,228/255,1)
            Rectangle(pos=c_label.pos,size = c_label.size)
        with s_label.canvas.before:
            Color(33/255,42/255,228/255,1)
            Rectangle(pos=s_label.pos,size = s_label.size)
        # Change current position for next row. Add Labels to FloatLayout
        self.CurrentPosition = (0,self.CurrentPosition[1]-100)
        self.add_widget(p_label)
        self.add_widget(c_label)
        self.add_widget(s_label)
     
    # Generate rows depending on data in database  
    def generateRows(self):
        self.allData = db.getAllData()
        print(self.allData)
        for i in self.allData:
            self.addRows(i)
        self.allData = None


    def generatePage(self):
        # Create Label and Buttons for the page. Put them in specific locations
        self.ViewTitle = Label(text="Application Submission History",pos=(50,500),size=(750,100),size_hint=(None,None))
        self.jobLabel = Label(text="Job Position",pos=(0,400), size=(266,100),size_hint=(None,None))
        self.companyLabel = Label(text="Company",pos=(266,400), size=(266,100),size_hint=(None,None))
        self.submissionLabel = Label(text="Date of Submission",pos=(532,400), size=(266,100),size_hint=(None,None))
        self.returnButton = Button(text="Home Page", pos=(0,500),size=(200,100),size_hint=(None,None))
        self.clearButton = Button(text="Clear All", pos=(600,500), size=(200,100), size_hint=(None,None))
        # Bind Button to perform specific tasks when pressed
        self.returnButton.bind(on_press=self.viewToHome)
        self.clearButton.bind(on_press=self.clearAllEntries)
        # Position will be used to be determine where to put next row
        self.CurrentPosition = (0,300)
        # Use Canvas to put Rectangle at specific position and change color of background
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
        with self.clearButton.canvas.before:
            Color(33/255,42/255,228/255,1)
            Rectangle(pos=self.clearButton.pos,size = self.clearButton.size)
        # Add widgets to FloatLayout
        self.add_widget(self.ViewTitle)
        self.add_widget(self.jobLabel)
        self.add_widget(self.companyLabel)
        self.add_widget(self.submissionLabel)
        self.add_widget(self.returnButton)
        self.add_widget(self.clearButton)
        
class PotentialApplicationsPage(FloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # These lists are used to determine how to delete widgets
        self.p_labels = []
        self.c_labels = []
        self.l_labels = []
        self.s_labels = []
       
        # Create all the labels for basic structure
        self.titleLabel = Label(text="Potential Application Submissions", pos=(200,500), size=(400,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.positionLabel = Label(text="Position", pos=(0,400), size=(200,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.companyLabel = Label(text="Company", pos=(200,400), size=(200,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.locationLabel = Label(text="Location", pos=(400,400), size=(200,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.submissionLabel = Label(text="Completed?", pos=(600,400), size=(200,100), size_hint=(None,None),color = [0,0,0,1], font_size = '20sp')
        self.homeButton = Button(text="Return Home", pos=(0,500),size=(200,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.homeButton.bind(on_press=self.goHome)
        self.clearAllButton = Button(text="Clear All", pos=(600,500), size=(200,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.clearAllButton.bind(on_press=self.clearAll)
        
        # Use canvas to put labels in specific location
        with self.titleLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.titleLabel.pos, size=self.titleLabel.size)
        with self.positionLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.positionLabel.pos, size=self.positionLabel.size)
        with self.companyLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.companyLabel.pos, size=self.companyLabel.size)
        with self.locationLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.locationLabel.pos, size=self.locationLabel.size)
        with self.submissionLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.submissionLabel.pos, size=self.submissionLabel.size)
        with self.homeButton.canvas.before:
            Rectangle(pos=self.homeButton.pos, size=self.homeButton.size)
        with self.clearAllButton.canvas.before:
            Rectangle(pos=self.clearAllButton.pos, size=self.clearAllButton.size)
        with self.canvas.before:
            Color(216/255,69/255,30/255,1)
            Rectangle(pos=(0,0), size=(1000,400))

        # Put all widgets into  float layout. None of these widgets will change whether new material is added or deleted
        self.add_widget(self.titleLabel)
        self.add_widget(self.positionLabel)
        self.add_widget(self.companyLabel)
        self.add_widget(self.locationLabel)
        self.add_widget(self.submissionLabel)
        self.add_widget(self.homeButton)
        self.add_widget(self.clearAllButton)

        # Create a scroll object and settings
        self.scroll = ScrollView()
        
        self.scroll.scroll_timeout = 200
        self.scroll.size=(Window.width,Window.height)
        self.scroll.pos_hint={'top': .6665, 'center_x':0.5}
        self.scroll.bar_color=[0,0,0,1]
        self.scroll.bar_inactive_color = [0,0,0,1]
        self.scroll.bar_width = 10
        self.scroll.scroll_type=['bars', 'content']
        
        self.scroll.do_scroll_x = False
        self.scroll.do_scroll_y = True
        self.layout = GridLayout(size_hint=(1, None), height=100, pos_hint={'top': .6665, 'center_x':0.5}, cols=4)
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)
        

    def goHome(self,instance):
        jobApp.screen_manager.current="start"

    def clearAll(self,instance):
        # Create a popup with two buttons
        self.popup = Popup(title="Are you sure? Clearing all entries can not be undone.",size_hint=(None,None), size=(400,400))
        box = BoxLayout()
        yesButton = Button(text="Yes")
        noButton = Button(text = "No")
        # Bind the button to two options
        noButton.bind(on_press=self.popup.dismiss)
        yesButton.bind(on_press=self.deleteAllEntries)
        # Add buttons to popup widget
        box.add_widget(yesButton)
        box.add_widget(noButton)
        self.popup.content = box
        self.popup.open()

    def deleteAllEntries(self,instance):
        potentialAppsDB.deleteAllData()
        self.popup.dismiss()
        for i in range(self.length):
            self.a_layout.clear_widgets([self.p_labels[i], self.l_labels[i], self.s_labels[i], self.c_labels[i]])
        self.p_labels = []
        self.c_labels = []
        self.l_labels = []
        self.s_labels = []
        
    def generateRows(self):
        self.allData = potentialAppsDB.getAllData()
        self.length = len(self.allData)
        for i in self.allData:
            self.addRows(i)
        self.allData = None
       

    def addRows(self,allData):
        # Create labels that will hold the actual values from database
        self.p_label = Label(text=str(allData[0]),color = [0,0,0,1], font_size = '20sp')
        self.c_label = Label(text=str(allData[1]),color = [0,0,0,1], font_size = '20sp')
        self.l_label = Label(text=str(allData[2]),color = [0,0,0,1], font_size = '20sp')
        self.s_label = Label(text=str(allData[3]),color = [0,0,0,1], font_size = '20sp')
        self.p_labels.append(self.p_label)
        self.l_labels.append(self.l_label)
        self.c_labels.append(self.c_label)
        self.s_labels.append(self.s_label)
        # Create Recntangle and Change Color for each row
       
        # Change current position for next row. Add Labels to FloatLayout
        self.layout.height += 100
        self.layout.add_widget(self.p_label)
        self.layout.add_widget(self.c_label)
        self.layout.add_widget(self.l_label)
        self.layout.add_widget(self.s_label)
        
      
       

class enterApps(GridLayout):
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
        self.add_widget(Label(text="Location"))
        self.LocationInput = TextInput(multiline = False)
        self.add_widget(self.LocationInput)

         # User enters data when application was applied for
        self.add_widget(Label(text="Completed?"))
        self.CompletionInput = TextInput(multiline = False)
        self.add_widget(self.CompletionInput)

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
        popup = Popup(title='Submission Successful!',content=Button(text='Potential Job Application successfully stored. Click to close!'),size_hint=(None, None), size=(400, 400))
        popup.open()
        popup.content.bind(on_press=popup.dismiss)
        # Retrieve Data
        position = self.posInput.text
        company = self.companyInput.text
        location = self.LocationInput.text
        submitted = self.CompletionInput.text
        self.potentialApps = PotentialApps(position,company,location,submitted)
        potentialAppsDB.insertDB(self.potentialApps)
        # Clear text inputs
        self.posInput.text=''
        self.companyInput.text=''
        self.LocationInput.text=''
        self.CompletionInput.text=''
        potentialAppsDB.printDB()
     
    def go_home(self,instance):
        jobApp.screen_manager.current = "start"

class JobTrackerApp(App):
    def build(self):
        # Screen Manager manages all the screens in the application
        self.screen_manager = ScreenManager()
        #self.kvFile = Builder.load_file("C:\\Users\\18186\\source\\repos\\JobApplicationTrackerApp\\JobApplicationTrackerApp\\PotentialApplicationsPage.kv")
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
        # Add View Potential Applications
        self.potentialApps = PotentialApplicationsPage()
        screen4 = Screen(name="potentialApps")
        screen4.add_widget(self.potentialApps)
        self.screen_manager.add_widget(screen4)
        # Enter Potential Job Apps
        self.enterApps = enterApps()
        screen5 = Screen(name="enterApps")
        screen5.add_widget(self.enterApps)
        self.screen_manager.add_widget(screen5)
        return self.screen_manager

   
if __name__ == "__main__":
    jobApp = JobTrackerApp()
    db = userInfoDatabase()
    potentialAppsDB = potentialAppsDatabase()
    jobApp.run()
