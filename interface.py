import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import QTime, Slot, Qt
import time
import csv
import os

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


@Slot()
def edit_number_rows(value):
    if value > int(rows):
        value -= int(rows)
        for x in range(value):
            file_list.append(FileRow("00:00", "https://"))
            entry_layout.addLayout(file_list[-1].hlayout)
            rows.increment()
    elif value < int(rows):
        file_list[-1].hlayout.removeWidget(file_list[-1].linkbox)
        file_list[-1].hlayout.removeWidget(file_list[-1].timebox)
        file_list[-1].linkbox.deleteLater()
        file_list[-1].timebox.deleteLater()
        entry_layout.removeItem(file_list[-1].hlayout)
        file_list[-1].hlayout.deleteLater()
        file_list.pop()
        rows.decrement()

@Slot()
def save_form():
    os.remove("classes.csv")
    with open("classes.csv", "w+") as csvfile:
        writer = csv.writer(csvfile)

        days = []
        for checkbox in DOWSelector.checkboxes:
            if checkbox.isChecked():
                days.append(checkbox.text())
        writer.writerow(days)

        to_remove = []
        for x in file_list:
            write_time = x.timebox.time().toString("HH:mm")
            write_text = x.linkbox.text()
            if not write_text == "https://":
                # write to the file
                writer.writerow([write_time, write_text])
            else:
                # remove the entry from the layout to match the file
                x.hlayout.removeWidget(x.timebox)
                x.hlayout.removeWidget(x.linkbox)
                x.linkbox.deleteLater()
                x.timebox.deleteLater()
                entry_layout.removeItem(x.hlayout)
                x.hlayout.deleteLater()
                rows.decrement()
                to_remove.append(x)
        for i in to_remove:
            file_list.remove(i)

    numberClasses.setValue(rows)

#Initialize window and layout
app = QApplication(sys.argv)
stylesheet = open("Darkeum.qss")
app.setStyleSheet(stylesheet.read())
window = QWidget()
layout = QVBoxLayout()
entry_layout = QVBoxLayout()

numberClasses = QSpinBox()
# numberClasses.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Maximum)

layout.addWidget(numberClasses)

layout.addLayout(entry_layout)
layout.addStretch(0)
DOWSelector = DaysOfWeekSelector()


rows = Counter()
numberClasses.valueChanged[int].connect(edit_number_rows)
file_list = []
with open("classes.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for day in next(reader):
        DOWSelector.checkboxes[day_to_index(day)].setChecked(True)

    for row in reader:
        try:
            file_list.append(FileRow(row[0], row[1]))
        except IndexError:
            continue
        entry_layout.addLayout(file_list[int(rows)].hlayout)
        rows.increment()



numberClasses.setValue(rows)

layout.addLayout(DOWSelector.hlayout)

submitButton = QPushButton(text="Save")
submitButton.clicked.connect(save_form)
layout.addWidget(submitButton)
window.setLayout(layout)
window.show()
app.exec_()