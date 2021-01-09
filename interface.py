import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import QTime, Slot, Qt, QTimer
from PySide2.QtGui import QIcon
import time
import csv
import os
import manual
import asyncio
from HackJA2021.assignementPage import AssignmentPage

#Custom stuff
from custom_qt import *
from counter import Counter


def day_to_index(input):
    translate = {
        "Sun": 0,
        "Mon": 1,
        "Tue": 2,
        "Wed": 3,
        "Thu": 4,
        "Fri": 5,
        "Sat": 6
    }
    return translate[input]

def load_from_file(filename, rows):
    with open(filename, "r") as csvfile:
        file_list = []
        reader = csv.reader(csvfile)

        for row in reader:
            try:
                file_list.append(FileRow(row[0], row[1]))
                for day in row[2:]:
                    file_list[-1].dow.checkboxes[day_to_index(day)].setChecked(True)
            except IndexError:
                continue
            entry_layout.addLayout(file_list[int(rows)].hlayout)
            rows.increment()
        return file_list


@Slot()
def edit_number_rows(value):
    if value > int(rows):
        value -= int(rows)
        for x in range(value):
            file_list.append(FileRow("00:00", "https://"))
            entry_layout.addLayout(file_list[-1].hlayout)
            rows.increment()
    elif value < int(rows):
        for x in range(int(rows)-value):
            file_list[-1].clear()
            file_list.pop()
            rows.decrement()

@Slot()
def save_form():
    os.remove("classes.csv")
    with open("classes.csv", "w+") as csvfile:
        writer = csv.writer(csvfile)

        to_remove = []
        for x in file_list:

            write_time = x.timebox.time().toString("HH:mm")
            write_text = x.linkbox.text()
            if not write_text == "https://":
                days = []
                for day in x.dow.checkboxes:
                    if day.isChecked():
                        days.append(day.text())
                # write to the file
                writer.writerow([write_time, write_text] + days)
            else:
                # remove the entry from the layout to match the file
                x.clear()
                rows.decrement()
                to_remove.append(x)
        for i in to_remove:
            file_list.remove(i)

    numberClasses.setValue(rows)
@Slot()
def open_class_wrapper():
    manual.open_class()

@Slot()
def run_app():
    if runButton.text() != "Running...":
        timer.start()
        runButton.setText("Running...")
    else:
        timer.stop()
        runButton.setText("Run")

@Slot()
def minimize():
    window.hide()
    trayIcon.show()

def foreground():
    window.show()
    trayIcon.hide()


#Initialize window and layout
app = QApplication(sys.argv)
stylesheet = open("Darkeum.qss")
app.setStyleSheet(stylesheet.read())
layout = QVBoxLayout()
layout.setSizeConstraint(QLayout.SetMinimumSize)
entry_layout = QVBoxLayout()
entry_layout.setSizeConstraint(QLayout.SetFixedSize)
top_layout = QHBoxLayout()

numberClasses = QSpinBox()
top_layout.addWidget(QLabel(text="Number of Classes"))
top_layout.addWidget(numberClasses)
layout.addLayout(top_layout)

layout.addLayout(entry_layout)
layout.addStretch(0)

rows = Counter()
numberClasses.valueChanged[int].connect(edit_number_rows)

file_list = load_from_file("classes.csv", rows)

numberClasses.setValue(rows)


submitButton = QPushButton(text="Save")
submitButton.clicked.connect(save_form)
layout.addWidget(submitButton)

timer = QTimer()
timer.setInterval(5 * 1000)
timer.setTimerType(Qt.CoarseTimer)
timer.timeout.connect(open_class_wrapper)

runButton = QPushButton(text="Run")
runButton.clicked.connect(run_app)
layout.addWidget(runButton)

trayIcon = QSystemTrayIcon(QIcon("umbrella-icon.png"))
trayIcon.activated.connect(foreground)


minButton = QPushButton(text="Minimize")
minButton.clicked.connect(minimize)
layout.addWidget(minButton)
editPage = QWidget()
editPage.setLayout(layout)

assignmentPage = QWidget()
apage = AssignmentPage()
assignmentPage.setLayout(apage.layout)

editPage.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
window = QTabWidget()
window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
window.addTab(editPage, 'Edit Schedule')
window.addTab(assignmentPage, 'View Assignments')
window.show()

app.exec_()