from PySide2.QtCore import QTime, QSize
from PySide2.QtWidgets import QTimeEdit, QLineEdit, QHBoxLayout, QCheckBox
from PySide2.QtWidgets import QSizePolicy

class FileRow:

    def __init__(self, time, link):
        self.hlayout = QHBoxLayout()
        self.timebox = QTimeEdit(QTime.fromString(time))
        self.timebox.setDisplayFormat("HH:mm")
        self.linkbox = QLineEdit(link)
        self.linkbox.setMinimumSize(QSize(300, 24))
        self.hlayout.addWidget(self.timebox)
        self.hlayout.addWidget(self.linkbox)

class DaysOfWeekSelector:
    def __init__(self):
        self.hlayout = QHBoxLayout()
        labels = ["S", "M", "T", "W", "T", "F", "S"]
        self.checkboxes = []
        for x in labels:
            self.checkboxes.append(QCheckBox(text=x))
