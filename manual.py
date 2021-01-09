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

        for row in reader:
            if row == []:
                continue
            if currenttime == row[1]:
                print('Time correct')

                is_correct_day = False
                for day in row[2:]:
                    if day == time.strftime("%a"):
                        is_correct_day = True

                        if is_correct_day:
                            print("Opening...")
                            if row[2].startswith("https://") or row[2].startswith("http://"):
                                webbrowser.get("\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" %s").open(row[2])
                            else:
                                os.system(f"\"{row[1]}\"")
