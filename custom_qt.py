from PySide2.QtCore import QTime, QSize, Slot
from PySide2.QtWidgets import QTimeEdit, QLineEdit, QHBoxLayout, QCheckBox, QPushButton
from PySide2.QtWidgets import QSizePolicy
import webbrowser
import os


class FileRow:

    @Slot()
    def go_to_link(self):
        text = self.linkbox.text()
        if not text == "https://":
            if text.startswith("https://") or text.startswith("http://"):
                webbrowser.get("\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" %s").open(text)
            else:
                os.system(f"\"{text}\"")

    def __init__(self, time, link):
        self.hlayout = QHBoxLayout()
        self.timebox = QTimeEdit(QTime.fromString(time))
        self.timebox.setDisplayFormat("HH:mm")
        self.linkbox = QLineEdit(link)
        self.openbutton = QPushButton(text="Go")
        self.openbutton.clicked.connect(self.go_to_link)
        self.linkbox.setMinimumSize(QSize(300, 24))
        self.hlayout.addWidget(self.timebox)
        self.hlayout.addWidget(self.linkbox)
        self.hlayout.addWidget(self.openbutton)

class DaysOfWeekSelector:
    def __init__(self):
        self.hlayout = QHBoxLayout()
        labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        self.checkboxes = []
        for x in labels:
            new = QCheckBox(text=x)
            self.checkboxes.append(new)
            self.hlayout.addWidget(new)
