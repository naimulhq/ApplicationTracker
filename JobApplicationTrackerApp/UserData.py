class UserData:
    def __init__(self, jobPosition, company, submittedData):
        self.jobPosition = jobPosition
        self.company = company
        self.submittedData = submittedData
    
class PotentialApps:
    def __init__(self,jobPosition, company, location, submission):
        self.jobPosition = jobPosition
        self.company = company
        self.location = location
        self.submission = submission
