from datetime import datetime
import queue
from PyQt5 import QtCore
from PyQt5.QtWidgets import * # will limit once I know what I'm using

class WaitingQueueContentsLayout(QVBoxLayout):
    def __init__(self, label:str):
        super().__init__()

        # Set all spacing to 0
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        # Initialize member variables
        self.waitingCount = 0  # Assume there is nothing in queue at start
        self.longestWaitingStart = None

        # Initialize the labels for the waiting count and highest time
        self.waitingCountLabel = QLabel("x Waiting")
        self.waitingCountLabel.setObjectName("SubSectionHeader")
        self.waitingTimeLabel = QLabel("x:xx")
        self.waitingTimeLabel.setObjectName("SubSectionHeader")

        # Create the horizontal layour for the count and time
        lowerLayout = QHBoxLayout()
        lowerLayout.addWidget(self.waitingCountLabel)
        lowerLayout.addWidget(self.waitingTimeLabel)

        # Attach the layout below a descriptive label
        queueLabel = QLabel(label + ":")
        queueLabel.setObjectName("SectionHeader")
        self.addWidget(queueLabel)
        self.addLayout(lowerLayout)

        # Initialize a timer to keep track of the waiting time
        timer = QtCore.QTimer(self)

        # Attach the timer update method to the timer
        timer.timeout.connect(self.updateTimer)

        # Update the timer every second
        timer.start(1000)

    def updateQueue(self, count:int, longestStartTime:datetime):
        # Update the queue data
        self.waitingCount = count
        self.longestStartTime = longestStartTime

        # Update the labels
        self.waitingCountLabel.setText(str(self.waitingCount) + " Waiting")
        self.updateTimer()
    
    def updateTimer(self):
        if self.waitingCount > 0:
            # Convert the start time of the longest waiting into a timedelta
            longestWaitTime = datetime.now() - self.longestStartTime

            # Display the timedelta of the waiting contact
            minutes = longestWaitTime.seconds // 60
            seconds = longestWaitTime.seconds % 60
            self.waitingTimeLabel.setText("{:d}:{:02d}".format(minutes, seconds))
        else:
            # Just set to zero time if nobody is waiting
            self.waitingTimeLabel.setText("0:00")

class WaitingQueueFrame(QFrame):
    def __init__(self, label:str):
        super().__init__()
        self.setObjectName("SectionFrame")

        # Initialize and set the layout
        self.contentsLayout = WaitingQueueContentsLayout(label)
        self.setLayout(self.contentsLayout)

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
    
    def updatePositions(self, employees:dict[str, str]):
        # Iterate through each of the labels and update the name
        for posLabel in self.positionsLabels:
            # Get the position out of the label
            pos = posLabel.text().split(':')[0]

            # Update based on the name keyed by the position
            posLabel.setText(pos + ": " + employees[pos])

class QueueAndPositionState(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Initialize the three components of this layout
        self.phonesQueue = WaitingQueueFrame("Phones")
        self.bomgarQueue = WaitingQueueFrame("Bomgar")
        self.positions = Positions()

        # Attach the three components on this layout
        self.addWidget(self.phonesQueue)
        self.addWidget(self.bomgarQueue)
        self.addLayout(self.positions)
        self.addStretch()
    
    def updatePhones(self, count:int, longestStartTime:datetime):
        # Just call the method again on the phones queue
        self.phonesQueue.updateQueue(count, longestStartTime)

    def updateBomgar(self, count:int, longestStartTime:datetime):
        # Just call the method again on the bomgar queue
        self.bomgarQueue.updateQueue(count, longestStartTime)

    def updatePositions(self, employees:dict[str, str]):
        # Just call the method of positions
        self.positions.updatePositions(employees)