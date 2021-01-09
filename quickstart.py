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










def main():
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
        print((cid))  
        cname = course['name']
        metadata = service.courses().courseWork().list(courseId = cid).execute()
    

        print(metadata.get("courseWork"))
        assignments = []
        for work in (metadata.get("courseWork")):
            print(work)
            aname = work.get("title")
            try:
                year = work.get("dueDate").get("year")
                month = work.get("dueDate").get("month")
                day = work.get("dueDate").get("day")

                hour = (work.get("dueTime").get("hours"))
                minute = work.get("dueTime").get("minutes")

                duedate = time( year, month, day, hour, minute)
                assignments.append(assignment(duedate, cname, cid, aname))
            except: pass

        classes.append(assignments)

        print(classes[0][0].__dict__["t"])




    log = open("log.txt", "w")
    if not courses:
        print('No courses found.')
    else:
        print('Courses:')
        for course in courses:
            log.write(str(metadata.get("courseWork")) + "\n")
            

            # metadata =  course_work_results = service.courses().courseWork().list(courseId = course[u'id']).execute()

if __name__ == '__main__':
    main()

