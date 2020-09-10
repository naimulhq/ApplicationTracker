import sqlite3
from UserData import UserData
from UserData import PotentialApps

class userInfoDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('userInfo.db') # Creates a database connection. Either in memory or file storage. My implementation creates a db file to store data
        self.cur = self.conn.cursor() # Create a cursor which can be used to execute SQL statements

    def createDB(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                jobPosition text,
                company text,
                submissionData text
                )""")

    def insertDB(self,userdata):
        self.conn = sqlite3.connect('userInfo.db')
        self.cur.execute("INSERT INTO users VALUES (?,?,?)", (userdata.jobPosition, userdata.company, userdata.submittedData))
        self.conn.commit()
        self.conn.close()

    def printDB(self):
        self.cur.execute("SELECT * FROM users")
        print(self.cur.fetchall())

    def getAllData(self):
        self.cur.execute("SELECT * FROM users")
        return self.cur.fetchall()

    def deleteAllData(self):
        self.conn = sqlite3.connect('userInfo.db')
        self.cur.execute("DELETE FROM users")
        self.conn.commit()


class potentialAppsDatabase:
     def __init__(self):
        self.conn = sqlite3.connect('potentialAppsInfo.db') # Creates a database connection. Either in memory or file storage. My implementation creates a db file to store data
        self.cur = self.conn.cursor() # Create a cursor which can be used to execute SQL statements

     def createDB(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS potentialApps(
                jobPosition text,
                company text,
                submissionData text,
                submitted text
                )""")

     def insertDB(self,potentialApps):
        self.cur.execute("INSERT INTO potentialApps VALUES (?,?,?,?)", (potentialApps.jobPosition, potentialApps.company, potentialApps.location, potentialApps.submission))
        self.conn.commit()
      

     def printDB(self):
        self.cur.execute("SELECT * FROM potentialApps")
        print(self.cur.fetchall())

     def getAllData(self):
        self.cur.execute("SELECT * FROM potentialApps")
        return self.cur.fetchall()
        


  







# Commit changes and close
#cur.execute("INSERT into users VALUES ('Software Engineer', 'Facebook', '09/2/2020')")
#cur.execute("SELECT * FROM users WHERE jobPosition='Software Engineer'")
#print(cur.fetchone())




