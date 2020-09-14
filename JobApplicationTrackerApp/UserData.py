class UserData:
    def __init__(self, jobPosition, company, notified, interview, accepted):
        self.jobPosition = jobPosition
        self.company = company
        self.notified = notified
        self.interview = interview
        self.accepted = accepted
    
class PotentialApps:
    def __init__(self,jobPosition, company, location, submission):
        self.jobPosition = jobPosition
        self.company = company
        self.location = location
        self.submission = submission
