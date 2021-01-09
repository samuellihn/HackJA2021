from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.me', 'https://www.googleapis.com/auth/classroom.courses.readonly']

class time:
    def __init__(self, year, month, day, hour, minute,):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
class assignment:
    def __init__(self, t, ClassName, ClassID, AssignmentName):
        self.t = t
        self.ClassName = ClassName
        self.ClassID = ClassID
        self.AssignmentName = AssignmentName
    def __str__(self):
        print(f"Name:{ClassName}, ClassID: {ClassID}, Due Date:{t}, AssignmentName:{AssignmentName}")










def get_assignments():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])
    classes = []

    for course in courses:
        cid = course['id']
        print(course['name'],cid)
        cname = course['name']
        metadata = service.courses().courseWork().list(courseId = cid).execute()
    

        print(metadata.get("courseWork"))
        assignments = []
        if metadata.get("courseWork"):
            for work in (metadata.get("courseWork")):
                print(work)
                aname = work["title"]
                try:
                    year = work["dueDate"]["year"]
                    month = work["dueDate"]["month"]
                    day = work["dueDate"]["day"]

                    hour = work["dueTime"]["hours"]
                    minute = work["dueTime"]["minutes"]

                    duedate = time( year, month, day, hour, minute)
                    date = f"{month}/{day}/{year} {hour}:{minute}"
                    #Append due date, assignment name, and class name to assignment
                    assignments.append([course['name'], date, aname])
                except: pass

        classes.append(assignments)
        print(f"{str(assignments)}")
        #print(classes.__dict__)


    log = open("log.txt", "w")
    if not courses:
        print('No courses found.')
    else:
        print('Courses:')
        for course in courses:
            log.write(str(metadata.get("courseWork")) + "\n")
            

            # metadata =  course_work_results = service.courses().courseWork().list(courseId = course[u'id']).execute()
    return assignments
print(get_assignments())
