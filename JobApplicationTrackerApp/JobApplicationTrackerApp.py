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
        self.add_widget(Label(text="Notified"))
        self.NotifiedInput = TextInput(multiline = False)
        self.add_widget(self.NotifiedInput)

        # User enters data when application was applied for
        self.add_widget(Label(text="Interview"))
        self.InterviewInput = TextInput(multiline = False)
        self.add_widget(self.InterviewInput)

        # User enters data when application was applied for
        self.add_widget(Label(text="Accepted"))
        self.AcceptedInput = TextInput(multiline = False)
        self.add_widget(self.AcceptedInput)

        # Added a Home Button
        self.backButton = Button(text="Return to Home Page",font_size=14)
        self.backButton.bind(on_press=self.go_home)
        self.add_widget(self.backButton)

        # Create a submit button
        self.submitButton = Button(text="Submit", font_size=14)
        r,g,b= 33,42,228
        self.submitButton.background_color = [float(r)/255,float(g)/255,float(b)/255,1]
        self.submitButton.bind(on_press=self.submit_info) # When button is pressed, will go to method submitInfo
        self.add_widget(self.submitButton)

    # Notifies user that submission was successful
    def submit_info(self,instance):
        # Get all of the values from input
        popup = Popup(title='Submission Successful!',content=Button(text='Application successfully stored. Click to close!'),size_hint=(None, None), size=(400, 400))
        popup.open()
        popup.content.bind(on_press=popup.dismiss)
        # Retrieve Data
        position = self.posInput.text
        company = self.companyInput.text
        notified = self.NotifiedInput.text
        interview = self.InterviewInput.text
        accepted = self.AcceptedInput.text
        self.userData = UserData(position,company,notified,interview,accepted)
        # Insert to database
        db.insertDB(self.userData)
        # Clear text inputs
        self.posInput.text=''
        self.companyInput.text=''
        self.NotifiedInput.text=''
        self.InterviewInput.text=''
        self.AcceptedInput.text=''
    # Returns home when submit button is pressed
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

        self.viewFiledApps = Button(text="View Filed Application")
        self.viewFiledApps.bind(on_press=self.viewMyApps)

        self.viewPotentialApps = Button(text="View Potentials Job Applications")
        self.viewPotentialApps.bind(on_press=self.go_potential_apps)

        self.enterPotentialApps = Button(text="Enter Potentials Job Applications")
        self.enterPotentialApps.bind(on_press=self.enter_potential_apps)

        self.add_widget(self.infoButton)
        self.add_widget(self.enterPotentialApps)
        self.add_widget(self.viewFiledApps)
        self.add_widget(self.viewPotentialApps)

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
        self.length = len(db.getAllData())
        self.generatePage()
    
    def generatePage(self):
        # These lists are used to determine how to delete widgets
        self.index = 0
        self.p_labels = []
        self.c_labels = []
        self.l_labels = []
        self.s_labels = []
        self.optionButtons = []
        # Create all the labels for basic structure
        self.titleLabel = Label(text="Application Submissions\nTotal: " + str(self.length), pos=(200,500), size=(800,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.positionLabel = Label(text="Position", pos=(0,400), size=(300,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.companyLabel = Label(text="Company", pos=(300,400), size=(300,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.notifiedLabel = Label(text="Notified?", pos=(600,400), size=(175,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.interviewLabel = Label(text="Interview?", pos=(775,400), size=(175,100), size_hint=(None,None),color = [0,0,0,1], font_size = '20sp')
        self.acceptedLabel = Label(text="Accepted?", pos=(950,400), size=(175,100), size_hint=(None,None),color = [0,0,0,1], font_size = '20sp')
        self.homeButton = Button(text="Return Home", pos=(0,500),size=(300,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.homeButton.bind(on_press=self.goHome)
        self.clearAllButton = Button(text="Clear All", pos=(1000,500), size=(300,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.optionLabel = Label(text="Option", pos = (1125,400), size = (175,100),size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.clearAllButton.bind(on_press=self.clearAll)
        
        # Use canvas to put labels in specific location
        with self.titleLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.titleLabel.pos, size=self.titleLabel.size)
        with self.optionLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.optionLabel.pos, size=self.optionLabel.size)
        with self.positionLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.positionLabel.pos, size=self.positionLabel.size)
        with self.companyLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.companyLabel.pos, size=self.companyLabel.size)
        with self.notifiedLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.notifiedLabel.pos, size=self.notifiedLabel.size)
        with self.interviewLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.interviewLabel.pos, size=self.interviewLabel.size)
        with self.homeButton.canvas.before:
            Rectangle(pos=self.homeButton.pos, size=self.homeButton.size)
        with self.clearAllButton.canvas.before:
            Rectangle(pos=self.clearAllButton.pos, size=self.clearAllButton.size)
        with self.acceptedLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.acceptedLabel.pos, size=self.acceptedLabel.size)
        with self.canvas.before:
            Color(216/255,69/255,30/255,1)
            Rectangle(pos=(0,0), size=(1300,400))

        # Put all widgets into  float layout. None of these widgets will change whether new material is added or deleted
        self.add_widget(self.titleLabel)
        self.add_widget(self.positionLabel)
        self.add_widget(self.companyLabel)
        self.add_widget(self.interviewLabel)
        self.add_widget(self.notifiedLabel)
        self.add_widget(self.acceptedLabel)
        self.add_widget(self.homeButton)
        self.add_widget(self.clearAllButton)
        self.add_widget(self.optionLabel)

        # Create a scroll object and settings
        self.scroll = ScrollView()
        
        self.scroll.scroll_timeout = 200
        self.scroll.size=(Window.width,Window.height)
        self.scroll.pos_hint={'top': .6665, 'center_x':0.5}
        self.scroll.bar_color=[0,0,0,0]
        self.scroll.bar_inactive_color = [0,0,0,0]
        self.scroll.bar_width = 20
        self.scroll.scroll_type=['bars','content']
        
        self.scroll.do_scroll_x = False
        self.scroll.do_scroll_y = True
        self.layout = GridLayout(size_hint=(1, None), height=100, pos_hint={'top': .6665, 'center_x':0.5}, cols=6)
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)
      
    def goHome(self,instance):
        jobApp.screen_manager.current="start"
        self.layout.clear_widgets()
        self.layout.height = 100

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
        db.deleteAllData()
        self.popup.dismiss()
        self.clear_widgets()
        self.generatePage()
        
    def generateRows(self):
        self.p_labels = []
        self.c_labels = []
        self.n_labels = []
        self.i_labels = []
        self.a_labels = []
        self.optionButtons = []
        self.allData = db.getAllData()
        self.length = len(self.allData)
        self.titleLabel.text="Application Submissions\nTotal: " + str(self.length)
        self.index = 0
        for i in self.allData:
            self.addRows(i)
            self.index += 1
        self.allData = None
        

    def addRows(self,allData):
        # Create labels that will hold the actual values from database
        self.p_label = Label(text=str(allData[0]),color = [0,0,0,1], font_size = '20sp')
        self.c_label = Label(text=str(allData[1]),color = [0,0,0,1], font_size = '20sp')
        self.n_label = Label(text=str(allData[2]),color = [0,0,0,1], font_size = '20sp')
        self.i_label = Label(text=str(allData[3]),color = [0,0,0,1], font_size = '20sp')
        self.a_label = Label(text=str(allData[4]),color = [0,0,0,1], font_size = '20sp')
        self.optionButton = Button(text="Delete/Edit",color = [0,0,0,1], font_size = '20sp', size = (150,100), size_hint=(None,None), id = str(self.index))
        self.optionButton.bind(on_press=self.Options)
        self.p_labels.append(self.p_label)
        self.c_labels.append(self.c_label)
        self.n_labels.append(self.n_label)
        self.i_labels.append(self.i_label)
        self.a_labels.append(self.a_label)
        self.optionButtons.append(self.optionButton)
        # Change current position for next row. Add Labels to FloatLayout
        self.layout.height += 100
        self.layout.add_widget(self.p_label)
        self.layout.add_widget(self.c_label)
        self.layout.add_widget(self.n_label)
        self.layout.add_widget(self.i_label)
        self.layout.add_widget(self.a_label)
        self.layout.add_widget(self.optionButton)

    def Options(self,instance):
        self.optionsPopup = Popup(title="Choose an option", size=(400,400), size_hint=(None,None))
        buttonBox = BoxLayout()
        deleteButton = Button(text="Delete")
        editButton = Button(text="Edit")
        deleteButton.bind(on_press=self.deleteSpecific)
        editButton.bind(on_press=self.editSpecific)
        buttonBox.add_widget(deleteButton)
        buttonBox.add_widget(editButton)
        self.optionsPopup.content = buttonBox
        self.delete_editVal = int(instance.id)
        self.optionsPopup.open()

    def deleteSpecific(self,instance):
        position = (self.p_labels[self.delete_editVal]).text
        company = (self.c_labels[self.delete_editVal]).text
        notified = (self.n_labels[self.delete_editVal]).text
        interview = (self.i_labels[self.delete_editVal]).text
        accepted = (self.a_labels[self.delete_editVal]).text
        db.deleteSpecific(position,company,notified,interview,accepted)
        self.clear_widgets()
        self.generatePage()
        self.generateRows()
        self.optionsPopup.dismiss()
    
    def editSpecific(self,instance):
        pass

        
class PotentialApplicationsPage(FloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.index = 0
        self.generatePage()

    def generatePage(self):
        # These lists are used to determine how to delete widgets
        self.index = 0
        self.p_labels = []
        self.c_labels = []
        self.l_labels = []
        self.s_labels = []
        self.optionButtons = []
        # Create all the labels for basic structure
        self.titleLabel = Label(text="Potential Application Submissions", pos=(200,500), size=(800,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.positionLabel = Label(text="Position", pos=(0,400), size=(287.5,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.companyLabel = Label(text="Company", pos=(287.5,400), size=(287.5,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.locationLabel = Label(text="Location", pos=(575,400), size=(287.5,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.submissionLabel = Label(text="Completed?", pos=(862.5,400), size=(287.5,100), size_hint=(None,None),color = [0,0,0,1], font_size = '20sp')
        self.homeButton = Button(text="Return Home", pos=(0,500),size=(300,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.homeButton.bind(on_press=self.goHome)
        self.clearAllButton = Button(text="Clear All", pos=(1000,500), size=(300,100), size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.optionLabel = Label(text="Option", pos = (1150,400), size = (150,100),size_hint=(None,None), color = [0,0,0,1], font_size = '20sp')
        self.clearAllButton.bind(on_press=self.clearAll)
        
        # Use canvas to put labels in specific location
        with self.titleLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.titleLabel.pos, size=self.titleLabel.size)
        with self.optionLabel.canvas.before:
            Color(33/255,80/255,228/255,1)
            Rectangle(pos=self.optionLabel.pos, size=self.optionLabel.size)
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
            Rectangle(pos=(0,0), size=(1300,400))

        # Put all widgets into  float layout. None of these widgets will change whether new material is added or deleted
        self.add_widget(self.titleLabel)
        self.add_widget(self.positionLabel)
        self.add_widget(self.companyLabel)
        self.add_widget(self.locationLabel)
        self.add_widget(self.submissionLabel)
        self.add_widget(self.homeButton)
        self.add_widget(self.clearAllButton)
        self.add_widget(self.optionLabel)

        # Create a scroll object and settings
        self.scroll = ScrollView()
        
        self.scroll.scroll_timeout = 200
        self.scroll.size=(Window.width,Window.height)
        self.scroll.pos_hint={'top': .6665, 'center_x':0.5}
        self.scroll.bar_color=[0,0,0,0]
        self.scroll.bar_inactive_color = [0,0,0,0]
        self.scroll.bar_width = 20
        self.scroll.scroll_type=['bars','content']
        
        self.scroll.do_scroll_x = False
        self.scroll.do_scroll_y = True
        self.layout = GridLayout(size_hint=(1, None), height=100, pos_hint={'top': .6665, 'center_x':0.5}, cols=5)
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)
      
    def goHome(self,instance):
        jobApp.screen_manager.current="start"
        self.layout.clear_widgets()
        self.layout.height = 100

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
        self.clear_widgets()
        self.generatePage()
        
    def generateRows(self):
        self.p_labels = []
        self.c_labels = []
        self.l_labels = []
        self.s_labels = []
        self.optionButtons = []
        self.allData = potentialAppsDB.getAllData()
        self.length = len(self.allData)
        print(self.length)
        print(self.allData)
        self.index = 0
        for i in self.allData:
            self.addRows(i)
            self.index += 1
        self.allData = None
        

    def addRows(self,allData):
        # Create labels that will hold the actual values from database
        self.p_label = Label(text=str(allData[0]),color = [0,0,0,1], font_size = '20sp')
        self.c_label = Label(text=str(allData[1]),color = [0,0,0,1], font_size = '20sp')
        self.l_label = Label(text=str(allData[2]),color = [0,0,0,1], font_size = '20sp')
        self.s_label = Label(text=str(allData[3]),color = [0,0,0,1], font_size = '20sp')
        self.optionButton = Button(text="Delete/Edit",color = [0,0,0,1], font_size = '20sp', size = (150,100), size_hint=(None,None), id = str(self.index))
        print(self.index)
        self.optionButton.bind(on_press=self.Options)
        self.p_labels.append(self.p_label)
        self.l_labels.append(self.l_label)
        self.c_labels.append(self.c_label)
        self.s_labels.append(self.s_label)
        self.optionButtons.append(self.optionButton)
        # Change current position for next row. Add Labels to FloatLayout
        self.layout.height += 100
        self.layout.add_widget(self.p_label)
        self.layout.add_widget(self.c_label)
        self.layout.add_widget(self.l_label)
        self.layout.add_widget(self.s_label)
        self.layout.add_widget(self.optionButton)

    def Options(self,instance):
        self.optionsPopup = Popup(title="Choose an option", size=(400,400), size_hint=(None,None))
        buttonBox = BoxLayout()
        deleteButton = Button(text="Delete")
        editButton = Button(text="Edit")
        deleteButton.bind(on_press=self.deleteSpecific)
        editButton.bind(on_press=self.editSpecific)
        buttonBox.add_widget(deleteButton)
        buttonBox.add_widget(editButton)
        self.optionsPopup.content = buttonBox
        self.delete_editVal = int(instance.id)
        self.optionsPopup.open()

    def deleteSpecific(self,instance):
        position = (self.p_labels[self.delete_editVal]).text
        location = (self.l_labels[self.delete_editVal]).text
        company = (self.c_labels[self.delete_editVal]).text
        submission = (self.s_labels[self.delete_editVal]).text
        potentialAppsDB.deleteSpecific(position,company,location,submission)
        self.clear_widgets()
        self.generatePage()
        self.generateRows()
        self.optionsPopup.dismiss()
    
    def editSpecific(self,instance):
        pass
        

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
        Window.size=(1300,600)
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
