from PySide2.QtWidgets import *
from HackJA2021.custom_qt import AssignmentRow
from HackJA2021.classroom import get_assignments

class AssignmentPage:
    def __init__(self):
        self.layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()

        self.header = QLabel("Assignments:")
        self.top_layout.addWidget(self.header)

        self.layout.addLayout(self.top_layout)

        self.entry_layout = QVBoxLayout()

        self.assignments = get_assignments()
        for ass in self.assignments:
            entry = AssignmentRow(ass[0], ass[1], ass[2])
            self.entry_layout.addLayout(entry.content)

        self.layout.addLayout(self.entry_layout)
        self.layout.addStretch(0)


