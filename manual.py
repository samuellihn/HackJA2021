import webbrowser
import csv
import time
import sched
import os
import asyncio

def open_class():
    print(time.time())
    with open("classes.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        currenttime = time.strftime("%H:%M")
        is_correct_day = False
        for day in next(reader):
            if day == time.strftime("%a"):
                is_correct_day = True

        print(is_correct_day)
        for row in reader:
            if row == []:
                continue
            if currenttime == row[0]:
                print('Time correct')
                if is_correct_day:
                    print("Opening...")
                    if row[1].startswith("https://") or row[1].startswith("http://"):
                        webbrowser.get("\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" %s").open(row[1])
                    else:
                        os.system(f"\"{row[1]}\"")
