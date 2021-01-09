import webbrowser
import csv
import time
import sched
import os

s = sched.scheduler(time.time, time.sleep)
def open_class():
    with open("classes.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        currenttime = time.strftime("%H:%M")
        is_correct_day = False
        for day in next(reader):
            if day == time.strftime("%a"):
                is_correct_day = True

        for row in reader:
            if row == []:
                break
            if currenttime == row[0]:
                if is_correct_day:
                    webbrowser.get("\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" %s").open(row[1])
    s.enter(60, 1, open_class)

open_class()
s.run()