from PyQt5 import QtGui
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class PhonesQueue(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.addWidget(QLabel("Phones:"))
        lowerLayout = QHBoxLayout()
        lowerLayout.addWidget(QLabel(str(3) + " Waiting"))
        lowerLayout.addWidget(QLabel("4:32"))
        self.addLayout(lowerLayout)


class BomgarQueue(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.addWidget(QLabel("Bomgar:"))
        lowerLayout = QHBoxLayout()
        lowerLayout.addWidget(QLabel(str(3) + " Waiting"))
        lowerLayout.addWidget(QLabel("2:22"))
        self.addLayout(lowerLayout)

class Positions(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.addWidget(QLabel("Student Leader: Braeden S."))
        self.addWidget(QLabel("Tier 2: Hayley J."))
        self.addWidget(QLabel("Email: Matthew Z."))
        self.addWidget(QLabel("Info Desk: Carter S."))
        self.addWidget(QLabel("Counter: Mohsin K."))

class QueueAndPositionState(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.addLayout(PhonesQueue())
        self.addLayout(BomgarQueue())
        self.addLayout(Positions())
