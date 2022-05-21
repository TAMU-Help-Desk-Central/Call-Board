from turtle import pos
from PyQt5 import QtGui
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class WaitingQueue(QVBoxLayout):
    def __init__(self, label:str):
        super().__init__()

        # Initialize the labels for the waiting count and highest time
        self.waitingCount = QLabel("x Waiting")
        self.waitingTime = QLabel("x:xx")

        # Create the horizontal layour for the count and time
        lowerLayout = QHBoxLayout()
        lowerLayout.addWidget(self.waitingCount)
        lowerLayout.addWidget(self.waitingTime)

        # Attach the layout below a descriptive label
        self.addWidget(QLabel(label + ":"))
        self.addLayout(lowerLayout)

class Positions(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Initialize a list of positions that will be displayed by the call board
        positions = ["Student Leader", "Tier 2", "Email", "Info Desk", "Counter"]

        # Initialize a list with a label for each position
        self.positionsLabels = [QLabel(pos + ": xxx") for pos in positions]

        # Add each label to the layout
        for posLabel in self.positionsLabels:
            self.addWidget(posLabel)

class QueueAndPositionState(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Initialize the three components of this layout
        phonesQueue = WaitingQueue("Phones")
        bomgarQueue = WaitingQueue("Bomgar")
        positions = Positions()

        # Attach the three components on this layout
        self.addLayout(phonesQueue)
        self.addLayout(bomgarQueue)
        self.addLayout(positions)
